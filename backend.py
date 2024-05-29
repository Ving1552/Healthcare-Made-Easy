from flask import Flask, render_template, request,redirect,url_for
import requests
import webbrowser
from experta import *
form_opened=False
no_data_flag = True
app = Flask(__name__)
### Helper functions ###
def multi_input(options=[]): # returns a list of user selected values
    choice = None
    options.append("none")
    while choice is None:
        print("0) none")
        for i in range(len(options)-1):
            print(f"{i+1}) {options[i]}")
        print("Your choice: ", end='')
        try:
            choice = [ int(x)-1 for x in input().split() ]
            for x in choice:
                if x >= len(options):
                    raise ValueError("Invalid value")
                if x == -1 and len(choice)>1:
                    raise ValueError("Can't have none and other values")
        except Exception as e:
            print("Invalid input. Try again")
            choice = None
    return [ options[i] for i in choice ]

def open_form(disease):
    # chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    url_string = f"http://127.0.0.1:5000/{disease}"
    webbrowser.get().open(url_string,new=0)
    # webbrowser.get('chrome').open_new("--incognito " + url_string)

@app.route('/displayResult',methods=['POST'])
def suggest_disease():
    open_doc = request.form['inp']
    disease=request.form['disease']
    if open_doc == "Yes":
       open_form(f'result/{disease}')
    
class MedicalExpert(KnowledgeEngine):
    @DefFacts()
    def _initial_action_(self):
        yield Fact(action="questionnaire")
    
    
    @app.route('/details', methods = ['POST'])
    @Rule(Fact(action="questionnaire"))
    def askBasicQuestions(self):
        try:
            self.declare(Fact(red_eyes=request.form['redeyes']))
            self.declare(Fact(fatigue=request.form['fatigue']))
            self.declare(Fact(short_breath=request.form['shortBreath']))
            self.declare(Fact(appetite_loss=request.form['appetite']))
            self.declare(Fact(fever=request.form['fever'])) 
            self.declare(Fact(chills=request.form['chills'])) 
            engine.run()
        except (KeyError,TypeError) as e:
            print("Error")

    @app.route('/submit_feedback', methods=['POST'])
    @Rule(AND(Fact(appetite_loss="no"), 
              Fact(fever="no"), 
              Fact(short_breath="no"),
              Fact(red_eyes="no"),
              Fact(chills="no"), 
              Fact(fatigue="no")))
    def hi(self):
        try:
            global form_opened
            if not form_opened:
                open_form("feedback")
                form_opened=True
                form_opened=False
        except:
             print("hlo")
    @app.route('/appetite', methods = ['POST'])
    @Rule(AND(Fact(appetite_loss="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(fatigue="no")))
    def askRelatedToAppetiteLoss(self):
        try:
            global form_opened
            if not form_opened:
                open_form("appetite_loss")
                form_opened=True
            self.declare(Fact(joint_pain=request.form['joint_pain']))
            self.declare(Fact(vomits=request.form['vomits'])) 
            form_opened=False
            engine.run()
        except (KeyError,TypeError) as e:
            print("Error")
            
    @app.route('/askPepticUlcer', methods = ['POST'])
    @Rule(AND(Fact(appetite_loss="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(fatigue="no"), Fact(vomits="Severe_Vomiting")))
    def askPepticUlcer(self):
        try:
            global form_opened
            if not form_opened:
                open_form("ulcer")
                form_opened=True
            burning_stomach=request.form['burning_stomach']
            bloating=request.form['bloating']
            mild_nausea=request.form['mild_nausea']
            weight_loss=request.form['weight_loss']
            abdominal_pain=request.form['abdominal_pain']
            form_opened=False
            count=0
            for string in [burning_stomach, bloating, mild_nausea, weight_loss, abdominal_pain]:
                if string=="yes":
                    count+=1

            if count>=3:
                symptoms = ["Appetite loss", "Severe Vomiting", "Burning sensation in stomach", "Bloated stomach", "Nausea", "Weight loss", "Abdominal pain"]
                return render_template('result.html',disease = "Peptic Ulcer", data =symptoms)
            return render_template('NoData.html')
        except (KeyError,TypeError) as e:
            print("Error")
   

    @app.route('/askArthritisRes', methods = ['POST'])
    @Rule(AND(Fact(appetite_loss="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(fatigue="no"), Fact(joint_pain="yes")))
    def askArthritis(self):
        global form_opened
        if not form_opened:
            open_form("arthritis")
            form_opened=True
        stiff_joint=request.form['stiff_joint']
        swell_joint=request.form['swell_joint']
        red_skin_around_joint=request.form['red_skin_around_joint']
        decreased_range=request.form['decreased_range']
        tired=request.form['tired']
        form_opened=False
        count=0
        for string in [stiff_joint, swell_joint, red_skin_around_joint, decreased_range, tired]:
            if string=="yes":
                count+=1
        if count>=3:
            symptoms = ["Stiff joints", "Swelling in joints", "Joint Pains", "Red skin around joints", "Tiredness", "Reduced Movement near joints", "Appetite loss"]
            if not form_opened:
                return render_template('result.html',disease = "Arthritis", data =symptoms)
        return render_template('NoData.html')
    
    @app.route('/askGastritisRes', methods = ['POST'])
    @Rule(AND(Fact(appetite_loss="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(fatigue="no"), Fact(vomits="Normal_Vomiting")))
    def askGastritis(self):
        global form_opened
        if not form_opened:
            open_form("gastritis")
            form_opened=True
        nausea=request.form['nausea']
        fullness=request.form['fullness']
        bloating=request.form['bloating']
        abdominal_pain=request.form['abdominal_pain']
        indigestion=request.form['indigestion']
        gnawing=request.form['gnawing']
        form_opened=False
        count=0
        for string in [nausea, fullness, bloating, abdominal_pain, indigestion, gnawing]:
            if string=="yes":
                count+=1

        if count>=4:
            symptoms = ["Appetite loss", "Vomiting", "Nausea", "Fullness near abdomen", "Bloating near abdomen", "Abdominal pain", "Indigestion" "Gnawing pain near abdomen"]
            if not form_opened:
                return render_template('result.html',disease = "Gastritis", data =symptoms)
        return render_template('NoData.html')
    
    @app.route('/askFatigue', methods = ['POST'])
    @Rule(AND(Fact(fatigue="yes"), Fact(fever="no"), Fact(short_breath="no")))
    def askRelatedToFatigue(self):
        global form_opened
        if not form_opened:
            open_form("fatigue")
            form_opened=True
        self.declare(Fact(extreme_thirst=request.form['extreme_thirst']))
        self.declare(Fact(extreme_hunger=request.form['extreme_hunger']))
        self.declare(Fact(dizziness=request.form['dizziness']))
        self.declare(Fact(muscle_weakness=request.form['muscle_weakness']))
        form_opened=False
        engine.run()
    
    @app.route('/askDiabetesRes', methods = ['POST'])
    @Rule(AND(Fact(fatigue="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(extreme_thirst="yes"), Fact(extreme_hunger="yes")))
    def askDiabetes(self):
        global form_opened
        if not form_opened:
            open_form("diabetes")
            form_opened=True
        frequent_urination=request.form['frequent_urination']
        weight_loss=request.form['weight_loss']
        irratability=request.form['irratability']
        blurred_vision=request.form['blurred_vision']
        frequent_infections=request.form['frequent_infections']
        sores=request.form['sores']
        form_opened=False
        count=0
        for string in [frequent_urination, weight_loss, irratability, blurred_vision, frequent_infections, sores]:
            if string=="yes":
                count+=1
        if count>=4:
            symptoms = ["Fatigue", "Extreme thirst", "Extreme hunger", "Weight loss", "Blurred vision", "Frequent infections", "Frequent urination", "Irritability", "Slow healing of sores"]
            if not form_opened:
                return render_template('result.html',disease = "Diabetes", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askDehydrationRes', methods = ['POST'])
    @Rule(AND(Fact(fatigue="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(extreme_thirst="yes"), Fact(dizziness="yes")))
    def askDehydration(self):
        global form_opened
        if not form_opened:
            open_form("dehydration")
            form_opened=True
        less_frequent_urination= request.form['less_frequent_urination']
        dark_urine= request.form['dark_urine']
        lethargy= request.form['lethargy']
        dry_mouth= request.form['dry_mouth']
        form_opened = False
        count=0
        for string in [less_frequent_urination, dark_urine, lethargy, dry_mouth]:
            if string=="yes":
                count+=1
        if count>=2:
            symptoms = ["Fatigue", "Extreme thirst", "Dizziness", "Dark urine", "Lethargic feeling", "Dry mouth", "Less frequent urination"]
            if not form_opened:
                    return render_template('result.html',disease = "dehydration", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askHypothyroidism', methods = ['POST'])
    @Rule(AND(Fact(fatigue="yes"), Fact(fever="no"), Fact(short_breath="no"), Fact(muscle_weakness="yes")))
    def askHypothoroidism(self):
        global form_opened
        if not form_opened:
            open_form("Hypothyroidism")
            form_opened=True
        depression=request.form['depression']
        constipation=request.form['constipation']
        feeling_cold=request.form['feeling_cold']
        dry_skin=request.form['dry_skin']
        dry_hair=request.form['dry_hair']
        weight_gain=request.form['weight_gain']
        decreased_sweating=request.form['decreased_sweating']
        slowed_heartrate=request.form['slowed_heartrate']
        pain_joints=request.form['pain_joints']
        hoarseness=request.form['hoarseness']
        form_opened=False
        count=0
        for string in [depression, constipation, feeling_cold, dry_skin, dry_hair, weight_gain, decreased_sweating, slowed_heartrate, pain_joints, hoarseness]:
            if string=="yes":
                count+=1

        if count>=7:
            symptoms = ["Fatigue", "Muscle weakness", "Depression", "Constipation", "Cold feeling", "Dry skin", "Dry hair", "Weight gain", "Decreased sweating", "Slow heart rate", "Joint pains", "Hoarseness in voice"]
            if not form_opened:
                return render_template('result.html',disease = "Hypothyroidism", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askShortBreath', methods = ['POST'])
    @Rule(AND(Fact(short_breath="yes"), Fact(fever="no")))
    def askRelatedToShortBreath(self):
        global form_opened
        if not form_opened:
            open_form("ShortBreath")
            form_opened=True
        self.declare(Fact(back_joint_pain=request.form['back_joint_pain']))
        self.declare(Fact(chest_pain=request.form['chest_pain']))
        self.declare(Fact(cough=request.form['cough']))
        self.declare(Fact(fatigue=request.form['fatigue']))
        self.declare(Fact(headache=request.form['headache']))
        self.declare(Fact(pain_arms=request.form['pain_arms']))
        form_opened=False
        engine.run()
    
    @app.route('/askObesity', methods = ['POST'])
    @Rule(AND(Fact(short_breath="yes"), Fact(fever="no"), Fact(back_joint_pain="yes")))
    def askObesity(self):
        global form_opened
        if not form_opened:
            open_form("Obesity")
            form_opened=True
        sweating=request.form['sweating']
        snoring=request.form['snoring']
        sudden_physical=request.form['sudden_physical']
        tired=request.form['tired']
        isolated=request.form['isolated']
        confidence=request.form['confidence']
        form_opened=False
        count=0
        for string in [sweating, snoring, sudden_physical, tired, isolated, confidence]:
            if string=="yes":
                count+=1

        if count>=4:
            symptoms = ["Shortness in breath", "Back and Joint pains", "High sweating", "Snoring habit", "Tireness", "Low confidence"]
            if not form_opened:
                return render_template('result.html',disease = "Obesity", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askAnemia', methods = ['POST'])
    @Rule(AND(Fact(short_breath="yes"), Fact(fever="no"), Fact(chest_pain="yes"), Fact(fatigue="yes"), Fact(headache="yes")))
    def askAnemia(self):
        global form_opened
        if not form_opened:
            open_form("Anemia")
            form_opened=True
        irregular_heartbeat=request.form['irregular_heartbeat']
        weakness=request.form['weakness']
        pale_skin=request.form['pale_skin']
        lightheadedness=request.form['lightheadedness']
        cold_hands_feet=request.form['cold_hands_feet']
        form_opened=False
        count=0
        for string in [irregular_heartbeat, weakness, pale_skin, lightheadedness, cold_hands_feet]:
            if string=="yes":
                count+=1

        if count>=3:
            symptoms = ["Shortness in breath", "Chest pain", "Fatigue", "Headache", "Irregular heartbeat", "Weakness", "Pale skin", "Dizziness", "Cold limbs"]
            if not form_opened:
                return render_template('result.html',disease = "Anemia", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askCAD', methods = ['POST'])
    @Rule(AND(Fact(short_breath="yes"), Fact(fever="no"), Fact(chest_pain="yes"), Fact(fatigue="yes"), Fact(pain_arms="yes")))
    def askCAD(self):
        global form_opened
        if not form_opened:
            open_form("CAD")
            form_opened=True
        heaviness=request.form['heaviness']
        sweating=request.form['sweating']
        dizziness=request.form['dizziness']
        burning=request.form['burning']
        form_opened=False
        count=0
        for string in [heaviness, sweating, dizziness, burning]:
            if string=="yes":
                count+=1

        if count>=2:
            symptoms = ["Shortness in breath", "Chest pain", "Fatigue", "Arm pains", "Heaviness", "Sweating", "Diziness", "Burning sensation near heart"]
            if not form_opened:
                return render_template('result.html',disease = "CAD", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askAsthma', methods = ['POST'])
    @Rule(AND(Fact(short_breath="yes"), Fact(fever="no"), Fact(chest_pain="yes"), Fact(cough="yes")))
    def askAsthma(self):
        global form_opened
        if not form_opened:
            open_form("Asthma")
            form_opened=True
        Wheezing=request.form['Wheezing']
        sleep_trouble=request.form['sleep_trouble']
        form_opened=False
        count=0
        for string in [Wheezing, sleep_trouble]:
            if string=="yes":
                count+=1

        if count>=1:
            symptoms = ["Shortness in breath", "Chest pain", "Cough", "Wheezing sound when exhaling", "Trouble sleep because of coughing or wheezing"]
            if not form_opened:
                return render_template('result.html',disease = "Asthma", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askChills', methods = ['POST'])
    @Rule(Fact(chills="yes"))
    def askRelatedToFever(self):
        global form_opened
        if not form_opened:
            open_form("Chills")
            form_opened=True
        self.declare(Fact(chest_pain=request.form['chest_pain']))
        self.declare(Fact(abdominal_pain=request.form['abdominal_pain']))
        self.declare(Fact(sore_throat=request.form['sore_throat']))
        self.declare(Fact(chillsShaky=request.form['chillsShaky']))
        self.declare(Fact(rashes=request.form['rashes']))
        self.declare(Fact(nausea=request.form['nausea']))
        form_opened=False
        engine.run()

    @app.route('/askBronchitisRes', methods = ['POST'])
    @Rule(Fact(fever="Low_Fever"))
    def askBronchitis(self):
        global form_opened
        if not form_opened:
            open_form("bronchitis")
            form_opened=True
        cough=request.form['cough']
        wheezing=request.form['wheezing']
        chillsShaky=request.form['chills']
        chest_tightness=request.form['chest_tightness']
        sore_throat=request.form['sore_throat']
        body_aches=request.form['body_aches']
        breathlessness=request.form['breathlessness']
        headache=request.form['headache']
        nose_blocked=request.form['nose_blocked']
        form_opened=False
        count=0
        for string in [headache, cough, wheezing, chillsShaky, chest_tightness, sore_throat, body_aches, breathlessness, nose_blocked]:
            if string=="yes":
                count+=1

        if count>=7:
            symptoms = ["Slight Fever", "Cough", "Wheezing", "Chills in body", "Tightness in chest", "Sore throat", "Body aches", "Headache", "Breathlessness", "Blocke nose"]
            if not form_opened:
                return render_template('result.html',disease = "Bronchitis", data =symptoms)
        return render_template('NoData.html')
      
    
    @app.route('/askDengueRes', methods = ['POST'])
    @Rule(Fact(fever="High_Fever"))
    def askDengue(self):
        global form_opened
        if not form_opened:
            open_form("dengue")
            form_opened=True
        headache=request.form['headache']
        eyes_pain=request.form['eyes_pain']
        muscle_pain=request.form['muscle_pain']
        joint_pain=request.form['joint_pain']
        nausea=request.form['nausea']
        rashes=request.form['rashes']
        bleeding=request.form['bleeding']
        diarrhea=request.form['diarrhea']
        form_opened=False
        count=0
        for string in [headache, eyes_pain, muscle_pain, joint_pain, nausea, rashes, bleeding]:
            if string=="yes":
                count+=1

        if count>=5 :
            if diarrhea!="yes":
                symptoms = ["High fever", "Headache", "Eye pain", "Muscle pain", "Joint pains", "Nausea", "Rashes", "Bleeding"]
                if not form_opened:
                    return render_template('result.html',disease = "Dengue", data =symptoms)
            else:
                symptoms = ["High fever", "Headache", "Eye pain", "Bodyaches","Diarrhea", "Nausea", "Rashes", "Bleeding"]
                if not form_opened:
                    return render_template('result.html',disease = "Typhoid", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askEyeStatusRes', methods = ['POST'])
    @Rule(Fact(red_eyes="yes"))
    def askEyeStatus(self):
        global form_opened
        if not form_opened:
            open_form("eyeStatus")
            form_opened=True
        eye_burn = request.form['eye_burn']
        eye_crusting = request.form['eye_crusting']
        eye_irritation = request.form[
             'eye_irritation']

        # Check conditions for Conjunctivitis
        if eye_crusting == "yes" or eye_burn == "yes":
            symptoms = ["Burning sensation in eyes", "Crusting of eyes", "Redness in eyes"]
            return render_template('result.html', disease="Conjunctivitis", data=symptoms)

        # Check conditions for Eye Allergy
        elif eye_irritation == "yes":
            symptoms = ["Irritation in eyes", "Redness in eyes"]
            return render_template('result.html', disease="Eye Allergy", data=symptoms)

        form_opened = False
        return render_template('NoData.html')

    @app.route('/askPancreatitisRes', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"), Fact(nausea="yes")))
    def askPancreatitis(self):
        global form_opened
        if not form_opened:
            open_form("pancreatitis")
            form_opened=True
        count=0
        upper_abdominal_pain=request.form['upper_abdominal_pain']
        abdominal_eat=request.form['abdominal_eat']
        heartbeat=request.form['heartbeat']
        weight_loss = request.form['weight_loss']
        oily_stool=request.form['oily_stool']
        for string in [upper_abdominal_pain, abdominal_eat, heartbeat, weight_loss, oily_stool]:
            if string=="yes":
                count+=1
        form_opened = False
        if count>=3:
            symptoms = ["Nausea", "Fever", "Upper abdominal pain", "Heartbeat", "Weight loss", "Oily and smelly stool"]
          
            if not form_opened:
                return render_template('result.html',disease = "Pancreatitis", data =symptoms)
        return render_template('NoData.html')
    
    @app.route('/askHIV', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"), Fact(rashes="yes")))
    def askHIV(self):
        global form_opened
        if not form_opened:
            open_form("HIV")
            form_opened=True
        count=0
        headache=request.form['headache']
        muscle_ache=request.form['muscle_ache']
        sore_throat=request.form['sore_throat']
        lymph=request.form['lymph']
        diarrhea=request.form['diarrhea']
        cough=request.form['cough']
        weigh_loss =request.form['weigh_loss']
        night_sweats=request.form['night_sweats']
        form_opened=False
        for string in [headache, muscle_ache, sore_throat, lymph, diarrhea, cough, weigh_loss, night_sweats]:
            if string=="yes":
                count+=1

        if count>=6:
            symptoms = ["Fever", "Rashes", "Headache", "Muscle ache", "Sore throat", "Swollen lymph nodes", "Diarrhea", "Cough", "Weight loss", "Night sweat"]
            if not form_opened:
                return render_template('result.html',disease = "HIV", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askTB', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"), Fact(chest_pain="yes"), Fact(fatigue="yes"), Fact(chillsShaky="yes")))
    def askTB(self):
        global form_opened
        if not form_opened:
            open_form("Tuberculosis")
            form_opened=True

        persistent_cough = request.form['persistent_cough']
        weigh_loss = request.form['weigh_loss']
        night_sweats= request.form['night_sweats']
        cough_blood= request.form['cough_blood']
        form_opened=False
        count=0
        for string in [persistent_cough, weigh_loss, night_sweats, cough_blood]:
            if string=="yes":
                count+=1

        if count>=2:
            symptoms=["fever", "chest pain", "fatigue", "loss of appetite","persistent cough"]
            if not form_opened:
                return render_template('result.html',disease = "Tuberculosis", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askInfluenza', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"), Fact(fatigue="yes"), Fact(sore_throat="yes")))
    def askInfluenza(self):
        global form_opened
        if not form_opened:
            open_form("Influenza")
            form_opened=True
        
        weakness=request.form['weakness']
        dry_cough=request.form['dry_cough']
        muscle_ache=request.form['muscle_ache']
        chillsShaky=request.form['chills']
        nasal_congestion=request.form['nasal_congestion']
        headache=request.form['headache']
        form_opened = False
        count=0
        for string in [weakness, dry_cough, muscle_ache, chillsShaky, nasal_congestion, headache]:
            if string=="yes":
                count+=1

        if count>=4:
            symptoms = ["Fever", "Fatigue", "Sore throat", "Weakness", "Dry cough", "Muscle aches", "Chills", "Nasal congestion", "Headache"]
            if not form_opened:
                return render_template('result.html',disease = "Influenza", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askHepatitis', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"),  Fact(fatigue="yes"), Fact(abdominal_pain="yes")))
    def askHepatitis(self):
        global form_opened
        if not form_opened:
            open_form("Hepatitis")
            form_opened=True
        flu_like=request.form['flu_like']
        dark_urine=request.form['dark_urine']
        pale_stool=request.form['pale_stool']
        weight_loss=request.form['weight_loss']
        jaundice=request.form['jaundice']
        form_opened = False
        count=0
        for string in [flu_like, dark_urine, pale_stool, weight_loss, jaundice]:
            if string=="yes":
                count+=1

        if count>=3:
            symptoms = ["Fever", "Fatigue", "Abdominal pain", "Flu like symptoms", "Dark urine", "Pale stool", "Weight loss", "Yellow eyes and skin(Jaundice)"]
            if not form_opened:
                return render_template('result.html',disease = "Hepatitis", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askPneumonia', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"),  Fact(chest_pain="yes"), Fact(short_breath="yes"), Fact(nausea="yes")))
    def askPneumonia(self):
        global form_opened
        if not form_opened:
            open_form("Pneumonia")
            form_opened=True
        short_breath=request.form['short_breath']
        sweat=request.form['sweat']
        rapid_breath=request.form['rapid_breath']
        cough=request.form['cough']
        diarrhea=request.form['diarrhea']
        form_opened = False
        count=0
        for string in [short_breath, sweat, rapid_breath, cough, diarrhea]:
            if string=="yes":
                count+=1

        if count>=3:
            symptoms = ["Fever", "Chest pain", "Shortness in breath", "Nausea", "Sweating with chills", "Rapid breathing", "Cough with phlegm", "Diarrhea"]
         
            if not form_opened:
                return render_template('result.html',disease = "Pneumonia", data =symptoms)
        return render_template('NoData.html')
    
    @app.route('/askMalaria', methods = ['POST'])
    @Rule(AND( Fact(chills="yes"), Fact(abdominal_pain="yes"), Fact(nausea="yes"),Fact(chillsShaky="yes")))
    def askMalaria(self):
        global form_opened
        if not form_opened:
            open_form("Malaria")
            form_opened=True
        headache=request.form['headache']
        sweat=request.form['sweat']
        cough=request.form['cough']
        weakness=request.form['weakness']
        muscle_pain=request.form['muscle_pain']
        back_pain=request.form['back_pain']
        form_opened = False
        count=0
        for string in [headache, sweat, weakness, cough, muscle_pain, back_pain]:
            if string=="yes":
                count+=1

        if count>=4:
            symptoms = ["Fever", "Chills", "Abdominal pain", "Nausea", "Headache", "Sweating", "Cough", "Weakness", "Muscle pain", "Back pain"]
            if not form_opened:
                return render_template('result.html',disease = "Malaria", data =symptoms)
        return render_template('NoData.html')
    @app.route('/askCorona', methods = ['POST'])
    @Rule(AND(Fact(chills="yes"), Fact(fatigue="yes"), Fact(short_breath="yes"), Fact(nausea="yes")))
    def askCorona(self):
        global form_opened
        if not form_opened:
            open_form("Corona")
            form_opened=True
        chills=request.form['chills']
        cough=request.form['cough']
        body_aches=request.form['body_aches']
        headache=request.form['headache']
        sore_throat= request.form['sore_throat']
        lose_smell=request.form['lose_smell']
        diarrhea=request.form['diarrhea']
        form_opened = False
        count=0
        for string in [chills, body_aches, headache, sore_throat, lose_smell, diarrhea]:
            if string=="yes":
                count+=1

        if count>=4:
            symptoms = ["Fever", "Fatigue", "Shortness in breath", "Nausea", "Chills", "Cough", "Body aches", "Headache", "Sorethroat", "Diarrhea", "Loose sense of taste/smell"]
            if not form_opened:
                return render_template('result.html',disease = "Corona Virus", data =symptoms)
        return render_template('NoData.html')

    @app.route('/validateUser', methods=['POST'])
    def validateUser():
            # Get the values from the submitted form
            email = request.form.get('email')
            password = request.form.get('password')

            # Your validation logic here (you might check against a database)
            # For simplicity, this example assumes a hardcoded user and password
            valid_email = 'john@gmail.com'
            valid_password = '123'

            valid_email2 = 'student@gmail.com'
            valid_password2 = '1234'


            if (email == valid_email and password == valid_password) or (email == valid_email2 and password == valid_password2):
                # Redirect to a success page or perform other actions
                return redirect(url_for('success'))
            else:
                # Redirect to a failure page or perform other actions
                return redirect(url_for('failure'))
            
    @app.route('/registerUser', methods=['POST'])
    def registerUser():
            # Get the values from the submitted form
            email = request.form.get('email')
            password = request.form.get('password')
            return render_template('SuccessRegisteration.html')
            

@app.route('/successReg')
def successReg():
    return render_template('SuccessRegisteration.html')        

           

@app.route('/success')
def success():
    return render_template('Userdetailspage.html')

@app.route('/loginError')
def failure():
    return render_template('LoginError.html')
@app.route('/Corona')
def corona():
        return render_template('Corona_QA.html')



@app.route('/Malaria')
def Malaria():
        return render_template('Malaria_QA.html')

@app.route('/Pneumonia')
def Pneumonia():
        return render_template('Pneumonia_QA.html')


@app.route('/Hepatitis')
def Hepatitis():
        return render_template('Hepatitis_QA.html')



@app.route('/Influenza')
def Influenza():
        return render_template('Influenza_QA.html')



@app.route('/Tuberculosis')
def tb():
        return render_template('TB_QA.html')



@app.route('/HIV')
def HIV():
        return render_template('HIV_QA.html')


@app.route('/eyeStatus')
def eyeStatus():
        return render_template('EyeStatus_QA.html')
@app.route('/pancreatitis')
def pancreatitis():
        return render_template('Pancreatitis_QA.html')
@app.route('/dengue')
def Dengue():
        return render_template('Dengue_QA.html')


@app.route('/bronchitis')
def bronchitis():
        return render_template('Bronchitis_QA.html')
@app.route('/typhoid')
def typhoid():
        return render_template('Typhoid_QA.html')


@app.route('/Asthma')
def Asthma():
        return render_template('Asthma_QA.html')



@app.route('/Anemia')
def Anemia():
        return render_template('Anemia_QA.html')
@app.route('/CAD')
def CAD():
        return render_template('CAD_QA.html')

    

@app.route('/Obesity')
def Obesity():
        return render_template('Obesity_QA.html')
@app.route('/Chills')
def chills():
        return render_template('Chills_QA.html')


@app.route('/')
def index():
    return render_template('Homepage.html')

@app.route('/run_engine', methods=['POST'])
def runEngine():
    engine.run()

@app.route('/Hypothyroidism')
def Hypothyroidism():
        return render_template('Hypothyroidism_QA.html')

@app.route('/redirect-to-login')
def redirect_to_login():
    return render_template('Loginpage.html')
@app.route('/redirect-to-signup')
def redirect_to_signup():
    return render_template('Signuppage.html')
@app.route('/result/<template_name>')
def disRes(template_name):
    return render_template(f'{template_name}.html')

@app.route('/arthritis')
def arthritis():
        return render_template('arthritis_QA.html')

@app.route('/gastritis')
def gastritis():
        return render_template('gastritis_QA.html')
@app.route('/ulcer')
def ulcer():
        return render_template('ulcer_QA.html')
@app.route('/dehydration')
def dehydration():
        return render_template('Dehydration_QA.html')


@app.route('/appetite_loss')
def appetite_loss():
        return render_template('appetite_loss.html')

@app.route('/fatigue')
def fatigue():
        return render_template('Fatigue_QA.html')
@app.route('/ShortBreath')
def ShortBreath():
        return render_template('ShortBreath_QA.html')


@app.route('/diabetes')
def diabetes():
        return render_template('Diabetes_QA.html')


@app.route('/feedback')
def notFound():
    return render_template('Feedback.html')

if __name__ == "__main__":
        engine = MedicalExpert()
        
        engine.reset()
        app.run(debug = True)
 
        
    


        