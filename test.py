from subprocess import Popen



filename = 'C:/Users/hlnatao/Desktop/you/easy-ocr/static/uploads/chinese.jpg'
process = Popen(["python", "model.py", '--pathImg', filename], shell=True)
process.wait()