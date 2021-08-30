# Predict-Queue-Wait-Time in a Hospital

We have all experienced waiting in long queues in hospital before we get treated. At times, it can be frustrating to wait and the patient's bad health adds the fuel to fire. But what if there is a way by which we can find out how much time we will have to wait in the hospital (based on live data) ?
This is where our project comes in which will tell us the approximate queue wait time even before you enter the hospital and an exact time once you register on hospital reception !

Considered Workflow in Hospital. 
1. Entry
2. Registration desk
3. Billing counter
4. Waiting Area
5. Doctor's cabin
6. Pharmacy
7. Exit

This web app has 4 features (and ways to use it explained in a sequence):

1. Doctor's Availability : While you are at home and if you feel any kind of health issue, you can login into our app and see this section where in every doctor's timetable and his working hours are displayed along with his qualification and his OPD. You can check the doctor's working hours and your free schedule (more important for office persons who have time constraint). If it matches, you may think of visiting the hospital . If not, you may see another slot.

2. Planning a Visit : Once your slot matches, you can also check an approximate time you will spend from walking in to the hospital to walking out of the hospital. You just have to enter the day on which you are visiting and at what time you wish to see which doctor and our app will give you an approximate total journey time.

3. Visit to Hospital and Prediction of Queue Wait Time : Once you are ok with the given approximate total journey time and it matches with your own schedule, you can visit the hospital. On the registration desk of hospital, you will be issued a one time RFID Card. The RFID Card has an unique identification number. The patient will be identified through this number only.
Note : At every stage (registration desk, billing counter, doctor's cabin) the RFID card given to the patient wil be scanned on the RFID Scanner placed at every desk by the present hospital clerks twice. Once when the process ( of registration, billing , doctor's consultation) starts and other time when the individual process ends. All this data of every patient will be stored in database and the same database will be used for prediction of queue wait time)

4. At the registration desk after your registration, once you recieve the RFID card , you will have to enter the RFID number in our app. Our app will show you your queue number for the doctor you want to visit and the time you will spend in waiting area before you see the doctor. This definitely will lower your frustration since you already know how much time you will have to wait.


5. Services Provided : In case while consultation is going on and doctor asks the patient to perform some XYZ test(s), the patient can see the cost of that particular test and the time required to perform it in advance.
