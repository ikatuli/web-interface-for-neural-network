from imageai.Classification import ImageClassification
#from imageai.Classification.Custom import CustomImageClassification
import time
import os

prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath("./models/resnet50_imagenet_tf.2.0.h5")
prediction.loadModel()


def start(path,name):
    print(name)

    start_time = time.time()
    report_text=[]

    #predictions, probabilities = prediction.classifyImage(os.path.join(path,name), result_count=4)
    predictions, probabilities = prediction.classifyImage(os.path.join(path,name), result_count=10) #result_count количество переменных класса
    report_text.append('--- Нейросеть работала '+str(time.time() - start_time)+'сек. ---')
    
    for each_prediction, each_probability in zip(predictions, probabilities):
        print(each_prediction, " : ", each_probability)
        report_text.append([each_prediction,each_probability]) #Вывод вероятности

    return report_text



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path' ,action='store',help='Путь к дериктории c изображениями')
    parser.add_argument('-o', '--object',action='store', help='Объект')
    parser.parse_args()

    #Присвоение значений из параметров.
    path = parser.parse_args().path
    objects = parser.parse_args().object

    #Получаем спиок png изображений из дериктории:
    images = list(filter(lambda x: x.endswith('.jpg'), os.listdir(path)))
    img_verification_list=[]

    for i in images:
        tmp=start(path,i)

        if tmp[1][0] == objects:
            img_verification_list.append(i)

    print(img_verification_list)

