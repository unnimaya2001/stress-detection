from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import cv2
from deepface import DeepFace
from statistics import mean

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

con = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='emotion')
cmd = con.cursor()

app = Flask(__name__)

emotions = []

app.secret_key = 'classified'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form['textfield']
        passwd = request.form['password']

        cmd.execute("SELECT * FROM `login` WHERE `username`='"+usr+"' AND `password`='"+passwd+"' ")
        result = cmd.fetchone()
        print(result)
        if result is not None:
            usertype = result[3]
            session['utype'] = usertype
            session['lid'] = result[0]
            if usertype == "admin":
                return redirect(url_for('adminHome'))
            elif usertype == "employee":
                return redirect(url_for('empHome'))
            elif usertype == "pending":
                return "<script>alert('Waiting For Admin Approval!'); window.location='/'</script>"
        else:
            return "<script>alert('Incorrect Username or Password!'); window.location='/'</script>"
    else:
        return render_template('login.html')


@app.route('/adminHome')
def adminHome():
    return render_template('admin.html')


@app.route('/empReg', methods=['GET', 'POST'])
def empReg():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        pos = request.form['pos']
        addr = request.form['address']
        passwd = request.form['passwd']

        cmd.execute("INSERT INTO login VALUES(NULL,'"+email+"','"+passwd+"','pending')")
        lid = con.insert_id()
        print(lid)

        cmd.execute("INSERT INTO `employees` VALUES(NULL, '"+str(lid)+"','"+name+"','"+phone+"','"+email+"','"+dob+"',\
        '"+gender+"','"+addr+"', '"+pos+"',NULL)")
        con.commit()

        return "<script>alert('Registration Successful');window.location='/'</script>"

    else:
        return render_template("employee-register.html")


@app.route('/requests', methods=['GET', 'POST'])
def requests():
    if request.method == 'POST':
        pass
    else:
        cmd.execute("SELECT `employees`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
        FROM `employees`,`login` WHERE `login`.`id`=`employees`.`log_id` AND `usertype`='pending'")
        res = cmd.fetchall()
        print(res)
        return render_template('requests.html', data=res)


@app.route('/dismiss/<lid>')
def dismiss(lid):
    print(lid)
    cmd.execute("DELETE u, uf FROM `employees` AS u JOIN `login` AS uf ON uf.`id`=u.`log_id` WHERE u.`log_id`='"+lid+"'")
    con.commit()
    return redirect(request.referrer)


@app.route('/approve/<lid>')
def approve(lid):
    cmd.execute("UPDATE `login` SET `usertype`='employee' WHERE `id`='"+lid+"'")
    cmd.execute("UPDATE `employees` SET `doj`=CURDATE() WHERE `log_id`='"+lid+"' ")
    con.commit()
    return redirect(request.referrer)


@app.route('/empView', methods=['GET', 'POST'])
def empView():
    if request.method == 'POST':
        pass
    else:
        cmd.execute("SELECT `employees`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
        FROM `employees`,`login` WHERE `login`.`id`=`employees`.`log_id` AND `usertype`='employee'")
        res = cmd.fetchall()
        print(res)
        return render_template('employee-list.html', data=res)


@app.route('/Admin_empProfile/<lid>')
def Admin_empProfile(lid):
    usr = 'admin'

    cmd.execute("SELECT `login`.`username` , `employees`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
    FROM `employees`, `login` WHERE `login`.`id`=`employees`.`log_id` AND `log_id`='"+str(lid)+"' ")
    res = cmd.fetchone()
    print(res)

    cmd.execute("SELECT * FROM `emotions` WHERE `eid`=3 ORDER BY `id` DESC")
    emo = cmd.fetchall()[0]
    print(emo)

    return render_template('emp-profile.html', data=res, emo=emo, usr=usr)


@app.route('/AdminLog/<lid>')
def AdminLog(lid):
    cmd.execute("SELECT * FROM `emotions` WHERE `eid`='"+str(lid)+"'")
    res = cmd.fetchall()
    print(res)
    return render_template('log.html', data=res)


@app.route('/empHome')
def empHome():
    return render_template('emp-home.html')


@app.route('/live', methods=['GET', 'POST'])
def live():
    global emotions
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        raise IOError("Cannot open Webcam")
    c = 0
    while True:
        ret, frame = vid.read()

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
        # print(result)
        emos = result['emotion']
        print(emos)
        angry = f"Angry : {round(emos['angry'], 2)}%"
        disgust = f"Disgust : {round(emos['disgust'], 2)}%"
        fear = f"Fear : {round(emos['fear'], 2)}%"
        happy = f"Happy : {round(emos['happy'], 2)}%"
        sad = f"Sad : {round(emos['sad'], 2)}%"
        surprise = f"Surprise : {round(emos['surprise'], 2)}%"
        neutral = f"Neutral : {round(emos['neutral'], 2)}%"

        emots = [round(emos['angry'], 2), round(emos['disgust'], 2), round(emos['fear'], 2), round(emos['happy'], 2),
                 round(emos['sad'], 2), round(emos['surprise'], 2), round(emos['neutral'], 2)]
        emotions.append(emots)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            emotion = result['dominant_emotion']

            cv2.putText(frame, f"Dominant Emotion : {emotion}", (int(x), int(y)), font, 1, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, angry, (int(x + w), int(y + 10)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, disgust, (int(x + w), int(y + 30)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, fear, (int(x + w), int(y + 50)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, happy, (int(x + w), int(y + 70)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, sad, (int(x + w), int(y + 90)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, surprise, (int(x + w), int(y + 110)), font, .6, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, neutral, (int(x + w), int(y + 130)), font, .6, (0, 255, 0), 2, cv2.LINE_4)

        cv2.imshow('Stress Monitoring', frame)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    aAvrge = round(mean([i[0] for i in emotions]), 2)
    dAvrge = round(mean([i[1] for i in emotions]), 2)
    fAvrge = round(mean([i[2] for i in emotions]), 2)
    hAvrge = round(mean([i[3] for i in emotions]), 2)
    sAvrge = round(mean([i[4] for i in emotions]), 2)
    xAvrge = round(mean([i[5] for i in emotions]), 2)
    nAvrge = round(mean([i[6] for i in emotions]), 2)

    cmd.execute(f"INSERT INTO `emotions` VALUES(NULL, '3', CURDATE(), CURTIME(), {aAvrge}, {dAvrge}, {fAvrge}, {hAvrge}, {sAvrge}, {xAvrge}, {nAvrge})")
    con.commit()

    vid.release()
    cv2.destroyAllWindows()
    emotions = []
    return redirect(request.referrer)


@app.route('/log')
def log():
    lid = session['lid']
    cmd.execute("SELECT * FROM `emotions` WHERE `eid`='"+str(lid)+"'")
    res = cmd.fetchall()
    print(res)
    return render_template('log.html', data=res)


@app.route('/empProfile')
def empProfile():
    usr = None
    lid = session['lid']
    cmd.execute("SELECT `login`.`username` , `employees`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
    FROM `employees`, `login` WHERE `login`.`id`=`employees`.`log_id` AND `log_id`='"+str(lid)+"' ")
    res = cmd.fetchone()
    print(res)

    cmd.execute("SELECT * FROM `emotions` WHERE `eid`=3 ORDER BY `id` DESC")
    emo = cmd.fetchall()[0]
    print(emo)

    return render_template('emp-profile.html', data=res, emo=emo, usr=usr)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
