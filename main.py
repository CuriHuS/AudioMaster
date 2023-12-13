import pygame
import sys
import time
import asyncio
import random


pygame.init()

class SoundMaster:
    def __init__(self, filename, start_time, end_time):
        self.soundlist = [[filename, start_time, end_time]] # Sound 목록
        self.soundIndex = 0 # 선택된 Sound index
        self.filename = filename # 현재 Sound filename
        self.start_time = start_time
        self.end_time = end_time

        # mp3 파일 로드
        self.sound = pygame.mixer.Sound(self.filename)

        # 재생 시간 계산
        self.duration = self.sound.get_length()
        #self.start_pos = self.start_time * self.frame_rate
        #self.end_pos = self.end_time * self.frame_rate

    def soundChange(self, index):
        self.soundIndex = index
        self.filename = self.soundlist[index][0]
        self.start_time = self.soundlist[index][1]
        self.end_time = self.soundlist[index][2]


    def fade_out(self, duration=300): # 페이드 아웃
        pygame.mixer.music.fadeout(duration)
        global isPunch
        isPunch=False

    def play(self): #일반적인 재생
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(self.start_time)


    async def Segmentplay(self, start, end): #일부분만 재생

        """
        start: 재생 시작 시간
        end: 재생 멈춤 시간

        ex)
        소리 파일이 0~230초 까지라면
        Segmentplay 메소드를 통해 10~11초 구간, 30초~33초 구간만 따로 재생 가능
        
        """
        if start < 0:
            start = 0
        if end > self.end_time:
            end = self.end_time
        

        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(start)
        try:
            while True:
                if end <= start + pygame.mixer.music.get_pos() / 1000:
                    self.set_volume(0)
                    break
        finally:
            self.fade_out()


    def stop(self): #재생 중지
        """
        mp3 파일 Stop
        """
        
        pygame.mixer.music.stop()

    def is_playing(self): # 파일 재생 중인지 여부
        """
            True: 재생 중
            False: 재생 중지
        """
        return pygame.mixer.music.get_busy()

    def get_position(self): # 파일 재생 위치 반환
        """
            재생 위치 (초)
        """
        return pygame.mixer.music.get_pos() / self.frame_rate
    def set_volume(self, volume):
        """
        볼륨을 설정합니다.
        Args:
            volume: 볼륨 (0.0 ~ 1.0)
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self.sound.set_volume(volume)

    def soundAdd(self, filename, start_time, end_time):
        """
        SoundMaster Instance에 새로운 sound 삽입
        Args:
            filename: 소리파일.확장자 -> str
            start_time: 시작 시간 -> int
            end_time: 끝 시간 -> int
        """
        self.soundlist.append([filename, start_time, end_time])

    def soundRemove(self, index):
        """
        soundList에 있는 소리파일 삭제
        args: index
        """
        self.soundlist.remove(self.soundlist[index])


# mp3 파일 경로
filename = "sample.ogg"

"""
clock = pygame.time.Clock()
frame_rate = 60
clock.tick(frame_rate)
"""

# 시작 시간 (초)
start_time = 0
# 종료 시간 (초)
end_time = 236
# SoundMaster 객체 생성

player = SoundMaster(filename, start_time, end_time)



# 재생 중지
#player.stop()


#############################################################################
#   Test
#############################################################################
# 화면 크기 설정
screen_width = 520
screen_height = 520

# 화면 생성
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("My Game")

# 사각형 색상 설정
rect_color = (255, 255, 255)

# 사각형 너비와 높이 설정
rect_width = 80
rect_height = 80

punch_list = [[0,0],[1,1],[2,2],[3,3],[4,4],[0,4],[1,3],[2,2],[3,1],[4,0],[1,0],[0,1],[2,0],[1,1],[0,2],[0,0],[1,1],[2,2],[3,3],[4,4],[0,4],[1,3],[2,2],[3,1],[4,0],[1,0],[0,1],[2,0],[1,1],[0,2]]

punch_list2 = []
count = 100 # 누를 횟수
for i in range(count):
    punch_list2.append([random.randrange(0,5), random.randrange(0,5)])

punch_turn = 0
isPunch = False

player.soundAdd("seesea.ogg", 0, 213)

# 화면을 계속해서 업데이트하는 루프
while True:
    
    # 키보드와 마우스 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 종료 이벤트 발생 시 종료
            pygame.quit()
            sys.exit()

    # 화면을 흰색으로 채우기
    screen.fill((0, 0, 0))

    # 사각형 그리기
    for y in range(5):
        for x in range(5):
            pygame.draw.rect(screen, rect_color, (x * rect_width + 20*(x+1), y * rect_height + 20*(y+1), rect_width, rect_height))
    click_x = punch_list[punch_turn][0] * rect_width + 20*(punch_list[punch_turn][0]+1)
    click_y = punch_list[punch_turn][1] * rect_height + 20*(punch_list[punch_turn][1]+1)
                                                        
    pygame.draw.rect(screen, (255,0,0), (click_x, click_y, rect_width, rect_height))
    
    get_press = pygame.mouse.get_pressed()[0]
    if click_x <= pygame.mouse.get_pos()[0] <= click_x + rect_width and click_y <= pygame.mouse.get_pos()[1] <= click_y + rect_height and get_press == 1:
        punch_turn += 1
        isPunch = True
        asyncio.run(player.Segmentplay(40+punch_turn, 41+punch_turn))
        player.soundChange(punch_turn%2)
    while isPunch:
        pygame.display.update()
        if isPunch == False:
            break

    # 화면 업데이트
    pygame.display.update()

    
