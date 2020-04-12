#코드 최초 작성일 2020-04-10
#by Chanhyo Lee
import json
import datetime
import re

#카카오톡 대화를 시간, 사람, 내용 데이터로 잘라서 저장하는 객체.
#pc 내보내기 모드는 만들려고했는데 무기한 연기되었습니다. (모바일과 달리 귀찮은 작업이 될것으로 예상)
class KakaotalkJsonParser:
    #KakaotalkJsonParser(filename, mod=('pc' or 'mobile'))
    def __init__(self, mod):
        try:
            if mod is not "pc" and mod is not "mobile":
                Exception(mod + " mod is not supported. only 'pc' and 'mobile' mod supported")
            self.mod = mod
        except Exception as e:
            print("err : " + e)

        if mod is "pc":
            self.date_form = re.compile("")
        elif mod is "mobile":
            self.date_form = re.compile("[0-9]{4}\.([0-9]| ){2}\.([0-9]| ){2}\. (오후|오전)([0-9]| ){2}:([0-9]| ){2}")
        
    
    def set_mod(self,mod):
        try:
            if mod is not "pc" and mod is not "mobile":
                Exception(mod + " mod is not supported. only 'pc' and 'mobile' mod supported")
            self.mod = mod
        except Exception as e:
            print("err : " + e)

        if mod is "pc":
            self.date_form = re.compile("")
        elif mod is "mobile":
            self.date_form = re.compile("[0-9]{4}\.([0-9]| ){2}\.([0-9]| ){2}\. (오후|오전)([0-9]| ){2}:([0-9]| ){2}")
        self.mod = mod

    #파일을 dict 형태로 파싱해서 반환합니다.
    def parse(self, filename):
        result = {};
        try:
            file = open(filename, 'r', encoding='UTF8')
        except Exception as e:
            print("err : " + e)
        lines = file.readlines()

        for line in lines:
            #line = line.encode("utf-8")
            #line = line.decode("utf-8")
            date = self.date_form.search(line)
            if not date:    #매칭을 찾지 못하였을때
                continue
            if date.start() is not 0:   #날짜가 처음에 나오지 않을 때
                continue
            date_string = date.group().replace("오전","AM").replace("오후","PM")
            date = datetime.datetime.strptime(date_string, "%Y. %m. %d. %p %I:%M")
            date_processed = str(date)
            speaker = re.compile(", [^:]* : ").search(line).group().replace(", ","").replace(" : ","")
            chat = re.compile(": .*").search(line).group().replace(": ","")
            #debuging code
            print(f"date:{date_processed} , id:{speaker}, content:{chat}")
            
            if date.strftime("%Y-%m-%d") not in result :
                result[date.strftime("%Y-%m-%d")] = []
            result[date.strftime("%Y-%m-%d")].append({"timestamp": str(date), "speaker": speaker, "chat": chat})
        return result

    #결과를 json 파일로 반환하는 함수
    #결과 파일을 열어보면 유니코드 코드가 두두두두 찍혀있는 끔찍한 광경을 보실 수 있습니다.
    #고쳐야하나?()
    def parse_to_json_file(self, filename_input, filename_output):
        json_file_name = filename_output + ".json"
        file_output = open(json_file_name, mode = "w", encoding="utf-8")
        json.dump(self.parse(filename_input), file_output)
        file_output.close()

#테스트용 코드
#k_parser = KakaotalkJsonParser("pc")
#pprint(k_parser.parse("filename.txt"))