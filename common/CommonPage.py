def dictFectchAll(cursor):
    #먼저 [] 으로 dict 타입으로 선언하고, for문을 통해 내부에 값들을 추가하고자한다. cursor.description 은 
    #실행된 커서에 들어가 있는 내용이 들어간다는 것이다.
    #이떄 col[0] for cor in cursor.description 을 통해 첫번째 열의 데이터를 들고온다는 것이다.
    #이는 즉, table에 등록된 인자들의 이름을 의미한다. 여기서는 id,title, writer,contents, wdate, hit 가 들어온다.
    columns = [col[0] for col in cursor.description]

    #for row in cursor.fetchall():
     #   print(row)

    # 이렇게 하면 각 인자안의 내용이 하나씩 출력되는 상황을 의미한다.
    # ex)  (9, '제목3', '임꺽정', '미나위마ㅜㅎ리마우히망ㅎ', 0, datetime.datetime(2020, 8, 24, 11, 46, 48))
    # 이런식으로 가져온다.
    #이후 아래의 내용은 dict 내용으로 이를 묶어서 dict 타입으로 만든다는
    return [dict(zip(columns,row)) for row in cursor.fetchall()]

import math
class CommonPage:
   def __init__(self, totalCont=1, curPage=1, pagesize=10 ):
        self.curPage = curPage 
        self.totalCount = totalCont
        self.totalPage = math.ceil(self.totalCount/pagesize) #ceil 특정값보다 더큰 정수값. 4.5 이면 5페이지이다 
        self.start_index = (curPage-1) // 10 * 10 +1 
        self.end_index = self.start_index + 10

        if self.end_index>=self.totalPage:
            self.end_index = self.totalPage+1 

        if curPage > 1:
            self.isPrev=True 
            self.previous_page_number=curPage-1
        else:
            self.isPrev=False 
            self.previous_page_number=1

        if curPage ==  self.totalPage:
            self.isNext = False 
            self.next_page_number=curPage
        else:
            self.isNext= True 
            self.next_page_number=curPage+1

        self.page_range = range(self.start_index, self.end_index) 
        