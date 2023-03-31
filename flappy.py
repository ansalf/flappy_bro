from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *

# Mendefinisikan konstanta FPS (Frame Per Second) yang memiliki nilai 30.
FPS = 30
# Mendefinisikan konstanta SCREENWIDTH yang memiliki nilai 288.
SCREENWIDTH = 288
# Mendefinisikan konstanta SCREENHEIGHT yang memiliki nilai 512.
SCREENHEIGHT = 512
# Mendefinisikan konstanta PIPEGAPSIZE yang memiliki nilai 100. Konstanta ini menentukan jarak antara bagian atas dan bagian bawah pipa.
PIPEGAPSIZE = 100
# Mendefinisikan konstanta BASEY yang memiliki nilai 0,79 kali SCREENHEIGHT. Konstanta ini menentukan posisi dasar dari permainan.
BASEY = SCREENHEIGHT * 0.79
# Mendefinisikan IMAGES, SOUNDS, dan HITMASKS sebagai kamus kosong.
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# Mendefinisikan variabel PLAYERS_LIST sebagai tuple yang berisi tuple-tuple. Setiap tuple dalam PLAYERS_LIST berisi path ke tiga gambar burung yang berbeda (upflap, midflap, dan downflap) untuk setiap burung. Ada tiga burung: merah, biru, dan kuning.
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# Mendefinisikan variabel BACKGROUNDS_LIST sebagai tuple yang berisi path ke dua gambar latar belakang yang berbeda. Ada gambar latar belakang siang hari dan malam.
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# Mendefinisikan variabel PIPES_LIST sebagai tuple yang berisi path ke dua gambar pipa yang berbeda. Ada gambar pipa hijau dan merah.
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

# Menggunakan statement try-except untuk mengecek apakah variabel xrange telah didefinisikan. Jika belum, maka definisikan xrange sebagai range.
try:
    xrange
except NameError:
    xrange = range

# Mendefinisikan fungsi main(). Pertama-tama, menginisialisasi pygame dan membuat objek FPSCLOCK untuk mengontrol frame rate game. Kemudian, membuat objek layar dengan ukuran yang telah ditentukan dan memberinya judul 'Flappy Bird'. Objek SCREEN dan FPSCLOCK diatur sebagai variabel global agar dapat diakses dari seluruh fungsi lain dalam program.


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # Mengisi nilai variabel IMAGES yang berupa dictionary dengan beberapa gambar yang dibutuhkan dalam game.
    # variabel IMAGES['numbers'] adalah tuple yang berisi 10 gambar angka (0-9) yang akan digunakan untuk menampilkan skor pemain.
    # Gambar angka dimuat menggunakan pygame.image.load() dan dikonversi menjadi alpha surface menggunakan convert_alpha() agar dapat ditampilkan dengan transparansi.
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    # variabel IMAGES['gameover'] adalah gambar yang akan ditampilkan saat permainan berakhir.
    # Gambar game over dimuat menggunakan pygame.image.load() dan dikonversi menjadi alpha surface menggunakan convert_alpha()
    # agar dapat ditampilkan dengan transparansi.

    IMAGES['gameover'] = pygame.image.load(
        'assets/sprites/gameover.png').convert_alpha()

    # variabel IMAGES['message'] adalah gambar pesan selamat datang yang akan ditampilkan saat game dimulai.
    # Gambar pesan selamat datang dimuat menggunakan pygame.image.load() dan dikonversi menjadi alpha surface menggunakan convert_alpha()
    # agar dapat ditampilkan dengan transparansi.

    IMAGES['message'] = pygame.image.load(
        'assets/sprites/message.png').convert_alpha()

    # variabel IMAGES['base'] adalah gambar lantai yang digunakan sebagai dasar dalam game.
    # Gambar lantai dimuat menggunakan pygame.image.load() dan dikonversi menjadi alpha surface menggunakan convert_alpha()
    # agar dapat ditampilkan dengan transparansi.

    IMAGES['base'] = pygame.image.load(
        'assets/sprites/base.png').convert_alpha()

    # Mengisi nilai variabel SOUNDS yang berupa dictionary dengan beberapa file audio yang dibutuhkan dalam game.
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

        # variabel SOUNDS diisi dengan file audio yang dibutuhkan dalam game. File audio di-load menggunakan pygame.mixer.Sound()
        # dan disimpan dalam dictionary SOUNDS. Setiap file audio diidentifikasi dengan kunci (key) unik, seperti 'die', 'hit', 'point', 'swoosh', dan 'wing',
        # sehingga nantinya file audio tersebut dapat diputar dengan memanggil kunci tersebut.
    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    # terdapat loop utama yang terus berjalan selama permainan sedang berlangsung. Pada loop ini, gambar latar belakang acak dipilih dari daftar BACKGROUNDS_LIST
    # menggunakan fungsi random.randint(), dan gambar tersebut dimuat menggunakan pygame.image.load() dan dikonversi ke surface dengan menggunakan convert().
    # Gambar tersebut kemudian disimpan dalam variabel IMAGES['background'] dan akan ditampilkan di layar.
    while True:
        # memilih background sprites acak
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(
            BACKGROUNDS_LIST[randBg]).convert()

        # memilih sprites pemain acak
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # memilih sprites pipa secara acak
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hitmask untuk pipa
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask funtuk pemain
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        # untuk menjalankan permainan Flappy Bird
        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # menginisialisasi indeks pemain yang akan di-blitted di layar.
    playerIndex = 0
    # menginisialisasi sebuah iterator yang akan digunakan untuk mengubah indeks pemain
    # setelah setiap iterasi ke-5. Fungsi cycle() membuat iterator tak terbatas yang berputar melalui iterable yang diberikan ([0, 1, 2, 1] dalam kasus ini).
    playerIndexGen = cycle([0, 1, 2, 1])
    # menginisialisasi counter yang akan digunakan untuk melacak jumlah iterasi.
    loopIter = 0

    # menginisialisasi koordinat x pemain.
    playerx = int(SCREENWIDTH * 0.2)
    # menginisialisasi koordinat y pemain sedemikian rupa sehingga terpusat secara vertikal.
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    # menginisialisasi koordinat x dari pesan yang akan ditampilkan di layar.
    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    # menginisialisasi koordinat y dari pesan yang akan ditampilkan di layar.
    messagey = int(SCREENHEIGHT * 0.12)

    # menginisialisasi koordinat x dari basis.
    basex = 0
    # menginisialisasi jumlah maksimum dimana basis dapat bergeser ke kiri.
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # untuk gerakan pemain naik-turun di layar selamat datang
    playerShmVals = {'val': 0, 'dir': 1}

    # sebuah loop yang akan terus dijalankan selama kondisi True (benar)
    while True:
        # sebuah loop untuk mengambil semua event yang terjadi di pygame, seperti input keyboard, mouse, dan lainnya
        for event in pygame.event.get():
            # jika event yang terjadi adalah pengguna menekan tombol close (keluar) pada window atau menekan tombol escape di keyboard,
            # maka pygame di-quit dan program keluar dengan menggunakan sys.exit()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # jika event yang terjadi adalah pengguna menekan tombol space atau tombol up di keyboard, maka akan diputar suara wing,
            # lalu fungsi akan mengembalikan sebuah dictionary yang berisi informasi mengenai posisi player (playery), posisi base (basex),
            # dan iterator untuk mengganti gambar player (playerIndexGen)
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

# jika loop ke-n terbagi habis dengan 5 (atau dalam kata lain, jika sudah terjadi 5 kali loop),
        # maka gambar player akan diubah dengan menggunakan playerIndexGen        
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
            # setiap kali loop dijalankan, loopIter akan di-increment dan jika loopIter mencapai 30, maka akan di-reset kembali menjadi 0
        loopIter = (loopIter + 1) % 30
        # menggeser posisi base sebanyak 4 piksel ke kiri setiap kali loop dijalankan
        basex = -((-basex + 4) % baseShift)
        # membuat efek goyang-goyang pada player menggunakan playerShm
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))
        # menampilkan gambar player pada posisi (playerx, playery + playerShmVals['val'])
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        # menampilkan pesan "Press space to jump" pada posisi (messagex, messagey)
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        # menampilkan gambar base pada posisi (basex, BASEY)
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        # memperbarui tampilan layar
        pygame.display.update()
        # mengatur frame rate dari game sesuai dengan nilai FPS yang telah didefinisikan sebelumnya.
        FPSCLOCK.tick(FPS)

# mendefinisikan fungsi mainGame yang memerlukan argumen movementInfo. Fungsi ini bertanggung jawab untuk menjalankan
# permainan sebenarnya setelah pemain memulai game.

def mainGame(movementInfo):
    # Membuat variabel score, playerIndex, dan loopIter dengan nilai awal 0.
    score = playerIndex = loopIter = 0
    # Mendapatkan generator indeks pemain yang telah dihitung pada showWelcomeAnimation() dan meletakkannya ke dalam variabel playerIndexGen.
    playerIndexGen = movementInfo['playerIndexGen']
    # Mengatur koordinat horizontal dan vertikal awal untuk pemain dengan playerx set ke 20% dari SCREENWIDTH dan playery diberikan nilai dari movementInfo yang diteruskan.
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    # Mengatur posisi awal basex dengan nilai dari movementInfo.
    basex = movementInfo['basex']
    # Menghitung jumlah maksimum pergeseran horizontal yang dapat dilakukan oleh permukaan tanah.
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # Mendapatkan dua pipa baru dari fungsi getRandomPipe(), yang masing-masing terdiri dari dua elemen, yaitu titik koordinat atas dan bawah dari pipa.
    newPipe1 = getRandomPipe()
    # Mendapatkan dua pipa baru lagi untuk menambahkan ke upperPipes dan lowerPipes.
    newPipe2 = getRandomPipe()

    # Mendefinisikan daftar koordinat x dan y untuk pipa atas.
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # Mendefinisikan daftar koordinat x dan y untuk pipa bawah.
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    # Menghitung waktu yang dibutuhkan untuk setiap iterasi game dalam satuan detik.
    dt = FPSCLOCK.tick(FPS)/1000
    # Menghitung kecepatan perpindahan pipa ke kiri dengan mengalikan -128 dengan waktu dt.
    pipeVelX = -128 * dt

    # kecepatan pemain, kecepatan maks, akselerasi ke bawah, akselerasi pada penutup    playerVelY = -9   # player's velocity along Y, default same as playerFlapped
    playerVelY = -9   # kecepatan pemain sepanjang Y, standarnya sama dengan playerFlapped
    playerMaxVelY = 10   # kecepatan maksimum sepanjang Y, kecepatan turun maksimum
    playerMinVelY = -8   # min vel sepanjang Y, kecepatan naik maks
    playerAccY = 1   # percepatan pemain ke bawah
    playerRot = 45   # rotasi pemain
    playerVelRot = 3   # kecepatan sudut
    playerRotThr = 20   # ambang rotasi
    playerFlapAcc = -9   # kecepatan pemain saat mengepak
    playerFlapped = False  # Benar saat pemain mengepak

    while True:
        # Ulangi semua peristiwa yang telah terjadi sejak iterasi terakhir dari putaran permainan.
        for event in pygame.event.get():
            # Jika acara tersebut adalah acara "keluar" atau pemain telah menekan tombol "escape", maka keluarlah dari permainan.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # Jika kejadian tersebut adalah kejadian "keydown" dan pemain telah menekan tombol "spasi" atau "atas", maka setel kecepatan vertikal
            # pemain ke akselerasi flap konstan, setel bendera boolean untuk menunjukkan bahwa pemain telah mengepak, dan memainkan efek suara "sayap".
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

        # Periksa apakah pemain menabrak pipa atau tanah.
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        # Jika pemain jatuh, kembalikan kamus yang berisi berbagai informasi keadaan permainan seperti posisi y pemain, apakah mereka jatuh ke tanah, posisi pipa dan skor pemain saat ini.
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(
            IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx, playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
        playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collides with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                                 player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(
                playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(
                playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


if __name__ == '__main__':
    main()
