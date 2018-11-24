import sys
from abc import abstractmethod
from time import sleep

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

# window_dict=dict() # 이름이 key, 객체가 value인 창 딕셔너리(창 관리, 이름으로 구별)

def place_widget_in_layout(layout, widgets, arrange="spread"):
    """
    레이아웃과 위젯을 받아 중심부에 등간격으로 배치합니다. (Stretch 이용)
    :parameter layout: 레이아웃입니다.
    :parameter widgets: 위젯들로 구성된 iterable 객체입니다.
    :return: None
    :Exception: 위젯이 아님/유효하지 않은 배치 방식임
    """
    arrange=arrange.lower() # 소문자화(비교를 위해)
    if arrange not in ("spread", "center", "front", "back", "wing_f", "wing_b"): # 배치 방식이 다음 중 없으면?
        raise Exception("Invalid arrangement.") # 예외 발생

    """
    spread: 고르게 분산
    center: 중심으로 쏠림
    front: 앞으로 쏠림 / back: 뒤로 쏠림
    wing_f, wing_b: 양쪽으로 갈라짐, 홀수 개 위젯일 때 f는 앞에, b는 뒤에 붙임
    """
    # 이하는 크게 신경쓰지 않아도 됨(배치 방법에 따라 위젯 적절히 나열하기)
    if "wing" in arrange:
        l=len(widgets)//2
        is_odd=(len(widgets)%2==1)
        for i in range(l):
            layout.addWidget(widgets[i])
        if is_odd and "f" in arrange: layout.addWidget(widgets[l]) 
        layout.addStretch(1)
        if is_odd and "b" in arrange: layout.addWidget(widgets[l])
        for i in range(l):
            layout.addWidget(widgets[i+l+(1 if is_odd else 0)])
    else:
        if arrange in ("spread", "back", "center"): layout.addStretch(1)
        for w in widgets:
            layout.addWidget(w)
            if arrange=="spread": layout.addStretch(1)
        if arrange in ("spread", "front", "center"): layout.addStretch(1)
    
    return

class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    Wind 클래스를 만들면 창이 띄워집니다.
    """
    def __init__(self, name, without_show=False):
        """
        생성자입니다. 
        띄울 창의 이름을 결정하며, 끝날 때 setup을 호출합니다.
        :parameter name: 창의 이름입니다.
        :parameter without_show: 창을 띄우지 않을 여부입니다. 
        """
        super().__init__() # 상위 클래스의 생성자 호출
        # window_dict[name]=self # 딕셔너리에 본인 추가하기
        self.name=name # 창의 이름 정하기
        self.without_show=without_show # 창을 생성하자마자 띄우지 않을 건가?
        self.strong=False # 되묻지 않고 닫을지에 대한 여부
        self.design() # 디자인
        self.setup() # 셋업

    # 디자인 메소드는 반드시 오버라이드해야 합니다. (추상 메소드)
    @abstractmethod
    def design(self):
        pass

    def setup(self):
        """
        창을 세팅하고 띄웁니다.
        하는 일: 창의 제목 설정, 창 보이기
        """
        self.setWindowTitle(self.name) # 창의 제목 지정
        if not self.without_show: # 안 띄우지 않기로 했으면
            self.show() # 보이기

    def closeEvent(self, QCloseEvent): # 창 닫기 이벤트(X자 누르거나 .close() 호출 시)
        if self.strong: # 만약 되묻지 않기로 했다면? 
            # del window_dict[self.name] # 딕셔너리에서 본인의 이름 제거
            QCloseEvent.accept() # 그냥 CloseEvent 수용
        else: # 되묻기
            # 메시지박스로 물어보기(Y/N), 그 결과를 ans에 저장
            ans=QMessageBox.question(self, "Confirm", "Do you want to quit?", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans==QMessageBox.Yes: # ~.Yes, ~.No는 상수여서 비교 가능
                # del window_dict[self.name] # 본인 이름 제거
                QCloseEvent.accept() # CloseEvent 수용
            else:
                QCloseEvent.ignore() # CloseEvent 거절

    def strong_close(self, QCloseEvent): # 강하게 닫기(물어봄 X)
        self.strong=True # 안 되묻기로 한 뒤
        self.close() # 닫는다(그냥 종료)

class Main_wind(Wind):
    """
    메인 윈도우입니다. Wind를 상속합니다.
    게임 플레이의 중추입니다.
    Main window에서 모든 부가 창으로 이동할 수 있습니다.
    """
    def design(self):
        """
        창을 디자인합니다. 
        하는 일: 레이아웃, 창 위치/크기 결정, 버튼/텍스트 띄우기
        """
        Balance_text=Text("Your Money", self, False, (0,0)) # 잔고
        Capacity_text=Text("Storage space", self, False, (0,0)) # 창고용량
        Prices_text=Text("Prices",self, False, (0,0)) # 가격
        Next_day_button=Push_button("Sleep", "Next day", self, False, (0,0)) # '다음 날' 버튼
        End_button=Quit_button("Quit","Changes will not be saved.",self,False,(0,0)) # '끝내기' 버튼

        top_box=QHBoxLayout()
        place_widget_in_layout(top_box,(Balance_text, Capacity_text, Prices_text))
        bottom_box=QHBoxLayout()
        place_widget_in_layout(bottom_box, (Next_day_button, End_button), "Back")

        vbox=QVBoxLayout()
        vbox.addLayout(top_box)
        vbox.addStretch(1)
        vbox.addLayout(bottom_box)

        self.setLayout(vbox)
        self.setGeometry(100,100,1300,800) # 위치, 크기

class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    """
    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        start_btn=Moveto_button("Start", "Start game.", self, Main_wind, "Main") # 게임 시작 버튼
        quit_btn=Close_button("Quit", "Quit game.", self) # 종료 버튼

        vmid_box=QVBoxLayout()
        place_widget_in_layout(vmid_box,(start_btn,quit_btn))
        
        self.setLayout(vmid_box)
        self.setGeometry(300,300,200,150) # 창 위치와 창 크기

class Push_button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    __init__의 매개변수로 이름과 툴팁, 띄울 Wind 클래스(혹은 그 상속)을 받습니다.
    """
    def __init__(self, name, tooltip, window, for_layout=True, location=(0,0)):
        """
        생성자입니다. __init__이 끝날 때 utility_set을 호출합니다.
        :parameter name: 버튼의 이름(내용)입니다.
        :parameter tooltip: 버튼의 툴팁입니다. (마우스 올리면 나오는 내용)
        :parameter window: 버튼이 위치하는 Wind 객체입니다.
        :parameter location: 위치(왼쪽, 위쪽 좌표 튜플)
        :parameter not_for_layout: 레이아웃에 쓸 거면 False(레이아웃은 위치 지정 X)
        """
        super().__init__(name,window) # 상위 클래스의 생성자 호출
        self.for_layout=for_layout
        self.design(tooltip,location) # 디자인하기
        self.window=window
        self.utility_set(window) # 기능 설정

    def design(self, tooltip, location):
        """
        버튼을 디자인합니다.
        하는 일: 버튼 툴팁 설정, 위치/크기 조정
        :parameter tooltip: 버튼 툴팁(마우스 올리면 나타나는 거)입니다.
        :parameter location: 버튼 위치입니다. 
        """
        self.setToolTip(tooltip) # 툴팁 설정
        if not self.for_layout:
            self.move(location[0], location[1]) # 위치 이동
            self.resize(self.sizeHint()) # 글씨에 따라 버튼 크기 조정

    # utility_set은 반드시 오버라이드해야 함
    @abstractmethod
    def utility_set(self, window):
        pass

class Link_button(Push_button):
    """
    눌리면 새 창을 띄우는 버튼 클래스입니다. Push_button을 상속합니다.
    """
    def __init__(self, name, tooltip, window, link_class, link_name, for_layout=True, location=(0,0)):
        # 상위 클래스로부터 오버라이드합니다.
        """
        :parameter link_class: 띄울 창의 클래스입니다.
        :parameter link_name: 띄울 창의 이름입니다.
        """
        self.window_info=(link_class, link_name) # 창의 정보를 튜플로 만들기
        super().__init__(name,tooltip,window,for_layout,location) # 상위 클래스의 생성자 호출

    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다.
        # try except 제거 시 2번 클릭됨
        # https://stackoverflow.com/questions/46747317/when-a-qpushbutton-is-clicked-it-fires-twice
        try:
            self.clicked.disconnect()
        except Exception:
            pass
        self.clicked.connect(self.open_new_window)
    
    def open_new_window(self):
        """
        새 창을 여는 메소드입니다.
        """
        self.link=self.window_info[0](self.window_info[1])

class Moveto_button(Link_button):
    """
    눌리면 다른 창으로 이동하는 버튼 클래스입니다. Link_button을 상속합니다.
    """
    def open_new_window(self):
        # 상위 메소드로부터 오버라이드합니다.
        super().open_new_window()
        self.window.strong_close(QCloseEvent)

class Close_button(Push_button):
    """
    창을 닫을 때 쓰는 버튼 클래스입니다. Push_button을 상속합니다. 
    """
    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다. 
        self.clicked.connect(window.strong_close) # 호출하는 window를 닫습니다. (강하게)

class Quit_button(Close_button):
    """
    프로그램을 종료할 때 버튼 클래스입니다. Close_button을 상속합니다. 
    """
    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다. 
        self.clicked.connect(QCoreApplication.instance().quit) # 버튼을 누르면 다 종료되도록

class Text(QLabel):
    """
    텍스트입니다. QLabel을 상속합니다.
    """
    def __init__(self, text, window, for_layout=True, location=(0,0)):
        """
        생성자입니다. 끝날 때 setup을 호출합니다. 
        :parameter text: 나타낼 텍스트
        :parameter window: 텍스트를 띄울 창
        :parameter location: 위치(튜플, 왼쪽 좌표, 위 좌표)
        """
        super().__init__(text,window) # 상위 클래스의 생성자 호출
        self.for_layout=for_layout
        self.setup(location) # 위치

    def setup(self, location):
        """
        텍스트를 세팅하고 띄웁니다. 
        """
        if not self.for_layout:
            self.move(location[0], location[1]) # 위치 설정
            self.resize(self.sizeHint()) # 크기 설정

if __name__=="__main__":
    app=QApplication(sys.argv) # application 객체 생성하기 위해 시스템 인수 넘김
    intro=Intro_wind("Intro")
    sys.exit(app.exec_()) # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료