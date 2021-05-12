from xlrd import open_workbook
import pymysql

from snsP import my_settings

mydict = {}

nameArr = ['entrc_busan', 'entrc_chungbuk', 'entrc_chungnam',
           'entrc_daegu', 'entrc_daejeon', 'entrc_gangwon',
           'entrc_gwangju', 'entrc_gyeongbuk', 'entrc_gyeongnam',
           'entrc_gyunggi', 'entrc_incheon', 'entrc_jeju',
           'entrc_jeonbuk', 'entrc_jeonnam', 'entrc_sejong',
           'entrc_seoul', 'entrc_ulsan']


def openFileTxt():
    cnt = 1
    for i in range(0, len(nameArr)):
        j = 0

        path1 = 'F:\\project\\sns2\\address_data\\'
        path1 = path1 + nameArr[i]+'.txt'
        file1 = open(path1, 'r')
        lines = file1.readlines()

        for line in lines:
            #print(line)

            k = line.split('|')

            for mlm in range(0,len(k)):
                if (k[mlm].find('\n')) != -1:
                    k[mlm] = k[mlm].replace('\n','')

            mydict[j] = k

            j = j + 1
            cnt = cnt +1
    print(cnt)


def openFileTxt1():
    cnt = 1
    j = 0

    path1 = 'F:\\project\\sns2\\address_data\\개선_도로명코드_전체분.txt'
    file1 = open(path1, 'r')
    lines = file1.readlines()

    for line in lines:
        # print(line)

        k = line.split('|')

        for mlm in range(0, len(k)):
            if (k[mlm].find('\n')) != -1:
                k[mlm] = k[mlm].replace('\n', '')

        mydict[j] = k

        j = j + 1
        cnt = cnt + 1
    print(mydict)
    print(cnt)



def import_xlsfile(xlsfilename):
    wb = open_workbook(filename=xlsfilename)
    sheet = wb.sheet_by_name('1. 총괄표(현행)')

    sido_nm_cn = ''
    sido_nm_eng = ''
    sigungu_nm_cn = ''
    sigungu_nm_eng = ''

    a = 0
    print("nrow")
    print(sheet.nrows)
    for i in range(sheet.nrows):
        row = sheet.row(i)
        if 1251 <= i < 1271:
            row = sheet.row(i)
            if row[3].value == '':
                sido_nm_eng = row[7].value
                sido_nm_cn = row[8].value
                print(sido_nm_cn, sido_nm_eng)
                continue

            if row[5].value == '':
                sigungu_nm_eng = row[7].value
                sigungu_nm_cn = row[8].value
                continue

            if row[5].value != '':
                # None                                   # A = row[0]
                sido_cd = str(row[1].value)[:-2]  # B = row[1] 대분류 ex) 11.0
                sido_nm = row[2].value  # C = row[2] 시도   ex) 서울특별시
                sigungu_cd = str(row[3].value)[:-2]  # D = row[3] 중분류
                sigungu_nm = row[4].value  # E = row[4] 시군구
                adm_dr_cd = str(row[5].value)[:-2]  # F = row[5] 소분류 == 행정구역코드 ex) 1101053.0
                adm_dr_nm = row[6].value  # G = row[6] 읍면동
                adm_dr_nm_eng = row[7].value  # H = row[7] 영문표기
                adm_dr_nm_cn = row[8].value  # I = row[8] 한자표기
                mydict[adm_dr_cd] = [sido_nm, sigungu_nm, adm_dr_nm, sido_nm_eng, sigungu_nm_eng, adm_dr_nm_eng,
                                     sido_nm_cn,
                                     sigungu_nm_cn, adm_dr_nm_cn, sido_cd, sigungu_cd]
                print(mydict[adm_dr_cd])
                print(sido_nm)
            else:
                print('-----------')
                print(row)
        else:
            if row[3].value == '':
                sido_nm_eng = row[7].value
                sido_nm_cn = row[8].value
                continue

            if row[5].value == '':
                sigungu_nm_eng = row[7].value
                sigungu_nm_cn = row[8].value
                continue

            if sido_nm_eng == '':
                continue

            if row[5].value is not None:
                # None                                   # A = row[0]
                sido_cd = str(row[1].value)[:-2]  # B = row[1] 대분류 ex) 11.0
                sido_nm = row[2].value  # C = row[2] 시도   ex) 서울특별시
                sigungu_cd = str(row[3].value)[:-2]  # D = row[3] 중분류
                sigungu_nm = row[4].value  # E = row[4] 시군구
                adm_dr_cd = str(row[5].value)[:-2]  # F = row[5] 소분류 == 행정구역코드 ex) 1101053.0
                adm_dr_nm = row[6].value  # G = row[6] 읍면동
                adm_dr_nm_eng = row[7].value  # H = row[7] 영문표기
                adm_dr_nm_cn = row[8].value  # I = row[8] 한자표기
                mydict[adm_dr_cd] = [sido_nm, sigungu_nm, adm_dr_nm, sido_nm_eng, sigungu_nm_eng, adm_dr_nm_eng,
                                     sido_nm_cn,
                                     sigungu_nm_cn, adm_dr_nm_cn, sido_cd, sigungu_cd]
                print(sido_nm)
            else:
                print('-----------')

    print('a: ', a)
    sheet = wb.sheet_by_name('법정동코드 연계 자료분석용')

    for i in range(sheet.nrows):
        row = sheet.row(i)
        # A = row[0]  시도
        # B = row[1]  시군구
        # C = row[2]  행정구역명
        # D = row[3]  행정동(행정기관명)
        # E = row[4]  법정동
        # F = row[5]  행정구역코드    <-- adm_dr_cd
        # G = row[6]  행정기관코드
        # H = row[7]  행정기관 생성일
        # I = row[8]  법정동 코드
        # J = row[9]  관할지역
        # K = row[10] 행정동 영문명칭
        # L = row[11] 비고
        try:
            adr_dr_arr = mydict[str(row[5].value)[:-2]]
            if len(adr_dr_arr) > 11:
                continue
            else:
                adr_dr_arr.append(str(row[6].value)[:-2])
        except IndexError:  # list index out of range
            print('IndexError')
            pass
        except KeyError:
            #print('KeyError')
            pass


def insert_into_mysql():
    '''
    mysql> desc korea_dong_pg_tbl;
    +----------------+-------------+------+-----+---------+-------+
    | Field          | Type        | Null | Key | Default | Extra |
    +----------------+-------------+------+-----+---------+-------+
    | adm_dr_cd      | varchar(7)  | NO   | PRI | NULL    |       |
    | sido_nm        | varchar(45) | NO   |     | NULL    |       |
    | sigungu_nm     | varchar(45) | NO   |     | NULL    |       |
    | adm_dr_nm      | varchar(45) | NO   |     | NULL    |       |
    | sido_nm_eng    | varchar(45) | YES  |     | NULL    |       |
    | sigungu_nm_eng | varchar(45) | YES  |     | NULL    |       |
    | adm_dr_nm_eng  | varchar(45) | YES  |     | NULL    |       |
    | sido_nm_cn     | varchar(45) | YES  |     | NULL    |       |
    | sigungu_nm_cn  | varchar(45) | YES  |     | NULL    |       |
    | adm_dr_nm_cn   | varchar(45) | YES  |     | NULL    |       |
    | sido_cd        | varchar(2)  | NO   |     | NULL    |       |
    | sigungu_cd     | varchar(5)  | NO   |     | NULL    |       |
    | adm_dr_cd2     | varchar(11) | NO   |     | NULL    |       |
    | geom           | geometry    | YES  |     | NULL    |       |
    | updated        | datetime    | NO   |     | NULL    |       |
    +----------------+-------------+------+-----+---------+-------+
    '''
    conn = pymysql.connect(host='localhost', user=my_settings.db_id, password=my_settings.db_pw,
                            db=my_settings.db_name, charset='utf8')
    curs = conn.cursor()
    lll = 1
    for key in mydict:
        arr = mydict[key]
        korea_nm = "\"%s\", \"%s\", \"%s\"" % (arr[0], arr[1], arr[2])
        eng_nm = "\"%s\", \"%s\", \"%s\"" % (arr[3], arr[4], arr[5])
        cn_nm = "\"%s\", \"%s\", \"%s\"" % (arr[6], arr[7], arr[8])
        codes1 = "\"%s\", \"%s\", \"%s\"" % (arr[9], arr[10], arr[11])
        codes2 = "\"%s\", \"%s\", \"%s\"" % (arr[12], arr[13], arr[14])
        codes3 = "\"%s\", \"%s\"" % (arr[15], arr[16])
        sql = "INSERT INTO entrc_sido VALUES( %s, %s, %s, %s, %s, %s);" \
              % ( korea_nm, eng_nm, cn_nm, codes1, codes2, codes3)
        curs.execute(sql)
        print('in : ' + str(lll))
        lll = lll + 1
    conn.commit()
    conn.close()


#import_xlsfile("addData1.xls")
#
openFileTxt1()
insert_into_mysql()