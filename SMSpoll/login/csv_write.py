import csv
import datetime

def csv_write(l,qid,test_id,crn):

    qid=str(qid)
    try:
        with open('/home/ssdiprojectfall2015/SMSpoll/media/result/result'+test_id+crn+'.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([datetime.datetime.now()])
            spamwriter.writerow(["Response for Q."+qid])
            for item in l:
                spamwriter.writerow([item])

    except Exception:
        with open('/home/ssdiprojectfall2015/SMSpoll/media/result/result'+test_id+crn+'.csv', 'w+') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([datetime.datetime.now()])
            spamwriter.writerow(["Response for Q."+qid])
            for item in l:
                spamwriter.writerow([item])
    spamwriter.close()
