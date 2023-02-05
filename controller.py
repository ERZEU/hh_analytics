import csv
import re
from matplotlib import pyplot as plt
import numpy as np
from parse import get_area, prepare_salary


class Function():
    def get_vac(self, name_vac, name_area):
        id_area = 113
        if name_area:
            id_area = get_area(name_area)

        return prepare_salary(name_vac, id_area)

    
    def show_zp(self, mas_vac):
        zp_ot = []
        zp_do = []
        for item in mas_vac:
            if item[4]:
                zp_ot.append(int(item[4]))
            if item[5]:
                zp_do.append(int(item[5]))
        
        self.zp_ot = sorted(zp_ot)
        self.zp_do = sorted(zp_do)
        if len(zp_do) > 0 and len(zp_ot) > 0:
            sredn = (sum(zp_ot, 0)/len(zp_ot) + sum(zp_do, 0)/len(zp_do))/2
            return str(int(sredn)), str(min(zp_ot)), str(max(zp_do))
        else:
            return '0','0','0'
    
    def graph_zp(self):
        plt.plot(self.zp_ot)
        plt.title('График З/П')
        plt.xlabel('Количество вакансий', color='gray')
        plt.ylabel('Размер З/П',color='gray')
                
        plt.plot(self.zp_ot, label='З/П от')
        plt.legend()
        plt.show()

        plt.plot(self.zp_do, label='З/П до')
        plt.legend()
        plt.show()


    def graph_names(self, mas_req):
        text = ''
        for st in mas_req:
            if isinstance(st, str):
                text += st
        text = text.lower()

        pattern = r'[a-zA-Z]+'
        mas_words = re.findall(pattern,text)
        dict_words = {}
        for word in mas_words:
            dict_words[mas_words.count(word)] = word
        result = dict(sorted(dict_words.items(), key=lambda x: x[0]))

        index = np.arange(len(result))
        values = list(result)
        plt.bar(index, values)
        plt.xticks(index+0.4, list(result.values()))
        plt.show() 

    def save(self, mas_vac): #проверено
        with open("vacancies_russ.csv", mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ";", lineterminator="\r")
            file_writer.writerow(["Название вакансии", "Ссылка", "Город" ,"Время публикации", "Зарплата от", "Зарплата до"])

            if mas_vac:
                for vac in mas_vac:
                    file_writer.writerow(vac)