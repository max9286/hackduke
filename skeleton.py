pose_to_use = 'Psi'


from openni import *
import math, pygame, SimpleCV
import time
import accordian, guitar,drums, violin
import theremin as tmin

instrument = 'drum' #guitar, violin, accordian, drum, theremin

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Head")


ctx = Context()
ctx.init()

kinectImage = ImageGenerator()
kinectImage.create(ctx)


depth = DepthGenerator()
depth.create(ctx)

tmn = tmin.Theremin()
# Create the user generator
user = UserGenerator()
user.create(ctx)
allUsers = {}
INDEX = 0
dist = 'dist'
i = 'i'
slope = 'slope'
oldX, oldY = 'oldX', 'oldY'
oldRX, oldRY = 'oldRX', 'oldRY' 
oldLX, oldLY = 'oldLX', 'oldLY'
chords = 'chords'
pitchVal, volumeVal = 'pitchVal', 'volumeVal'
dist = 'dist'
# Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap
t = None
# Declare the callbacks
def new_user(src, id):
    print "1/4 User {} detected. Looking for pose..." .format(id)
    pose_cap.start_detection(pose_to_use, id)

def pose_detected(src, pose, id):
    print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
    pose_cap.stop_detection(id)
    skel_cap.request_calibration(id, True)

def calibration_start(src, id):
    print "3/4 Calibration started for user {}." .format(id)

def calibration_complete(src, id, status):
    global INDEX
    if status == CALIBRATION_STATUS_OK:

        dist = 'dist'
        i = 'i'
        slope = 'slope'
        oldX, oldY = 'oldX', 'oldY'
        oldRX, oldRY = 'oldRX', 'oldRY' 
        oldLX, oldLY = 'oldLX', 'oldLY'
        chords = 'chords'
        pitchVal, volumeVal = 'pitchVal', 'volumeVal'
        dist = 'dist'

        user1 = {dist: 0, i: 0, slope: 0, oldX: 0, oldY: 0, oldRX: 0, oldRY: 0,\
                 oldLX: 0, oldLY: 0, chords: 0, pitchVal: 0, volumeVal: 0, dist: 0,\
                 'instrument': 'drums', 'time': time.time()}
        user2 = {dist: 0, i: 0, slope: 0, oldX: 0, oldY: 0, oldRX: 0, oldRY: 0,\
                 oldLX: 0, oldLY: 0, chords: 0, pitchVal: 0, volumeVal: 0, dist: 0,\
                 'instrument': 'guitar', 'time': time.time()}
        user3 = {dist: 0, i: 0, slope: 0, oldX: 0, oldY: 0, oldRX: 0, oldRY: 0,\
                 oldLX: 0, oldLY: 0, chords: 0, pitchVal: 0, volumeVal: 0, dist: 0,\
                 'instrument': 'accordian', 'time': time.time()}
        user4 = {dist: 0, i: 0, slope: 0, oldX: 0, oldY: 0, oldRX: 0, oldRY: 0,\
                 oldLX: 0, oldLY: 0, chords: 0, pitchVal: 0, volumeVal: 0, dist: 0,\
                 'instrument': 'violin', 'time': time.time()}

        usrs = [user1, user2, user3, user4]
        if usrs[INDEX]['instrument'] == 'theremin':
            tmn.start()
        print "4/4 User {} calibrated successfully! Starting to track." .format(id)

        allUsers[id] = usrs[INDEX]

        INDEX += 1       

        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)

def lost_user(src, id):
    print "--- User {} lost." .format(id)
    if allUsers[id]['instrument'] == 'theremin':
        tmn.stop()
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD 

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
# Register them
user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)

# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
ctx.start_generating_all()
print "0/4 Starting to detect users. Press Ctrl-C to exit."

t = time.time()



while True:
    # Update to next frame
    ctx.wait_and_update_all()
    image = kinectImage.get_raw_image_map_bgr()
    newImage = pygame.image.fromstring(image,(640,480),"RGB")
    finalImage = SimpleCV.Image(pygame.surfarray.array2d(newImage)).flipHorizontal()
    
    finalImage.save('asd.png')
    finalImage = pygame.image.load('asd.png')
    screen.blit(finalImage,(0,0))


    # if instrument == 'accordian':
    #     font=pygame.font.Font(None,30)
    #     # scoretext=font.render("Slope:"+str(slope), 1,(255,255,255))

    #     if allUsers[id][i] == 0:
    #         scoretext=font.render("DECRESING:", 1,(255,255,255))
    #     elif allUsers[id][i] == 1:
    #         scoretext=font.render("SAME:", 1,(255,255,255))
    #     else:
    #         scoretext=font.render("INCREASING:", 1,(255,255,255))
    # if instrument == 'violin':
    #     font=pygame.font.Font(None,30)

    #     slopetext=font.render(str(slope), 1,(255,255,255))
        
    #     screen.blit(slopetext, (500, 457))
    # if instrument == 'guitar':
    #     font=pygame.font.Font(None,30)

    #     slopetext=font.render("CHORDS: " + str(allUsers[id][chords]), 1,(255,255,255))
    #     if allUsers[id][dist] <60:
    #         disttext=font.render("NONE: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     elif allUsers[id][dist] < 132:
    #         disttext=font.render("C0: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     elif allUsers[id][dist] < 204:
    #         disttext=font.render("C1: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     elif allUsers[id][dist] < 276:
    #         disttext=font.render("C2: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     elif allUsers[id][dist] < 348:
    #         disttext=font.render("C3: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     else:
    #         disttext=font.render("C4: " + str(allUsers[id][dist]), 1,(255,255,255))
    #     screen.blit(slopetext, (500, 457))
    #     screen.blit(disttext, (0, 457))
    # if instrument == 'theremin':
    #     font=pygame.font.Font(None,30)

    #     volText=font.render("Volume: " + str(allUsers[id][volumeVal]), 1,(255,255,255))
    #     pitchText=font.render("Pitch: " + str(allUsers[id][pitchVal]), 1,(255,255,255))
    #     screen.blit(volText, (500, 457))
    #     screen.blit(pitchText, (0, 457))

   
    #     volume = [(400,400),(600,400)]
    #     pitch = [(100,150),(100,350)]
    #     v = [volume, pitch]
    #     for x in v:
    #         pygame.draw.line(screen, (255,0,0), x[0],x[1], 5)  
    for id in user.users:
        if skel_cap.is_tracking(id):
            # print id
            instrument = allUsers[id]['instrument']

            RH = skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
            LH = skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
            #determine key point for instrument
            if instrument == 'accordian' or instrument == 'theremin':
                KP = skel_cap.get_joint_position(id, SKEL_NECK)  #dont need this
                KP = KP.point
            elif instrument == 'guitar':
                KP1 = skel_cap.get_joint_position(id, SKEL_RIGHT_HIP)
                KP2 = skel_cap.get_joint_position(id, SKEL_LEFT_HIP)

                KP = [(KP1.point[x]+KP2.point[x])/2 for x in range(3)]
                KP = KP2.point
            elif instrument == 'violin':
                KP = skel_cap.get_joint_position(id, SKEL_NECK).point
            elif instrument == 'drum' or instrument == 'drums':
                KP1 = skel_cap.get_joint_position(id, SKEL_RIGHT_HIP)
                KP2 = skel_cap.get_joint_position(id, SKEL_LEFT_HIP)

                KP = [(KP1.point[x]+KP2.point[x])/2 for x in range(3)]


            LHCENTER = LH.point
            RHCENTER = RH.point


            RHnormalX = 640-int(((RH.point[0]+1000)/2000) * 640)
            RHnormalY = 480-int(((RH.point[1]+500)/1000) * 480)

            pygame.draw.circle(screen, (255,0,0), (RHnormalX,RHnormalY), 5, 4)
            LHnormalX = 640-int(((LH.point[0]+1000)/2000) * 640)
            LHnormalY = 480-int(((LH.point[1]+500)/1000) * 480)
            pygame.draw.circle(screen, (0,255,0), (LHnormalX,LHnormalY), 5, 4)


            KPnormalX = 640-int(((((KP[0]))+1000)/2000) * 640)
            KPnormalY = 480-int((((((KP[1]+500)/1000) * 480))))
            KPNORMAL = (KPnormalX, KPnormalY)
            pygame.draw.circle(screen, (0,0,255), (KPnormalX,KPnormalY), 5, 4)

            if instrument == 'accordian':
                pygame.draw.line(screen, (0,255,0), (LHnormalX, LHnormalY),(RHnormalX,RHnormalY), 1)
                tmpD = (LHnormalX - RHnormalX)**2 + (LHnormalY )
                if tmpD > allUsers[id][dist] + 5:
                    accordian.play("in")
                    i = 2
                elif tmpD < allUsers[id][dist] - 5:
                    i = 0
                    accordian.play("out")
                else:
                    i = 1
                    accordian.stop()
                allUsers[id][dist] = tmpD
            if instrument == 'guitar':
                pygame.draw.line(screen, (0,255,0), (RHnormalX, RHnormalY),(KPnormalX,KPnormalY), 1)
                allUsers[id][dist] = ((KPnormalY-RHnormalY)**2+(RHnormalX-KPnormalY)**2)**.5
               
                if intersect([LHnormalX, LHnormalY], (allUsers[id][oldX], allUsers[id][oldY]), [RHnormalX, RHnormalY], [KPnormalX, KPnormalY]):
                    allUsers[id][chords] += 1
                    
                    guitar.stop()
                    #dist 60-400
                    if allUsers[id][dist] <30:
                        pass
                    elif allUsers[id][dist] < 102:
                        guitar.play(4)
                    elif allUsers[id][dist] < 174:
                        guitar.play(3)
                    elif allUsers[id][dist] < 246:
                        guitar.play(2)
                    elif allUsers[id][dist] < 318:
                        guitar.play(1)
                    else:
                        guitar.play(0)
                pygame.draw.line(screen, (0,255,0), (allUsers[id][oldX], allUsers[id][oldY]),(LHnormalX,LHnormalY), 1)
                if time.time() - allUsers[id]['time'] > .1:
                    allUsers[id][oldX] = LHnormalX
                    allUsers[id][oldY] = LHnormalY
                    allUsers[id]['time'] = time.time()


            if instrument == 'drum' or instrument == 'drums':
                d1 = [(50,-70),(125,-70)]
                d2 = [(-50,-130),(30,-130)]
                d3 = [(-50,-80),(-155,-80)]
                CRASH = [(125,-130),(225,-130)]
                drumss = [d1, d2, d3, CRASH]

                for drum in drumss:
                    if intersect([LHnormalX, LHnormalY], [allUsers[id][oldLX],allUsers[id][oldLY]], add(KPNORMAL[:2],drum[0]),add(KPNORMAL[:2],drum[1])):
                        if allUsers[id][oldLY] < LHnormalY:
                            if drum == d1:
                                drums.play(1)
                            elif drum == d2:
                                drums.play(0)
                            elif drum == d3:
                                drums.play(4)
                            else:
                                drums.play(3)

                    if intersect([RHnormalX, RHnormalY], [allUsers[id][oldRX],allUsers[id][oldRY]], add(KPNORMAL[:2],drum[0]),add(KPNORMAL[:2],drum[1])):
                        if allUsers[id][oldRY] < RHnormalY:
                            if drum == d1:
                                drums.play(1)
                            elif drum == d2:
                                drums.play(0)
                            elif drum == d3:
                                drums.play(4)
                            else:
                                drums.play(3)  

                    pygame.draw.line(screen, (255,0,0), add(KPNORMAL[:2],drum[0]),add(KPNORMAL[:2],drum[1]), 5)
                if time.time() - allUsers[id]['time'] > .05:
                    allUsers[id][oldLX] = LHnormalX
                    allUsers[id][oldLY] = LHnormalY
                    allUsers[id][oldRX] = RHnormalX
                    allUsers[id][oldRY] = RHnormalY
                    allUsers[id]['time'] = time.time()
            if instrument == 'violin':
                # pygame.draw.line(screen, (0,255,0), (RHnormalX, RHnormalY),(KPnormalX,KPnormalY), 1)
                if time.time() - t > .1:
                    try:
                        slope = (KPnormalY-oldY)/(RHnormalX-oldX)
                    except:
                        slope = 0
                
                
                p1 = [KPnormalX, KPnormalY]
                p2 = [RHnormalX, RHnormalY]
                pygame.draw.line(screen, (0,255,0), p1, p2, 3)

                if time.time() > .25:
                    try:
                        slope = (LHnormalY-allUsers[id][oldY])/(LHnormalX-float(allUsers[id][oldX]))
                    except:
                        slope = -1
                    pygame.draw.line(screen, (0,255,0), (allUsers[id][oldX], allUsers[id][oldY]), (LHnormalX, LHnormalY), 3)
                    if slope != -1:
                        distMoved = ((allUsers[id][oldX] - LHnormalX)**2 + (allUsers[id][oldY] - LHnormalY)**2)**.5
                        handDist = ((KPnormalX - RHnormalX)**2 + (KPnormalY - RHnormalY)**2)**.5
                        if distMoved > 10:
                            # print handDist
                            if slope > -1 and slope < 3:
                                if handDist > 150:
                                    violin.stop()

                                    violin.play(0)
                                else:
                                    violin.stop()

                                    violin.play(1)

                            else:
                                if handDist > 150:
                                    violin.stop()

                                    violin.play(2)
                                else:
                                    violin.stop()

                                    violin.play(3)
                        else:
                            violin.stop()

                    allUsers[id][oldX], allUsers[id][oldY] = LHnormalX, LHnormalY


                #draw the bow
            if instrument == 'theremin':  #WHADDUP
                volume = [(400,400),(600,400)]
                pitch = [(100,150),(100,350)]
                v = [volume, pitch]
                for x in v:
                    pygame.draw.line(screen, (255,0,0), x[0],x[1], 5)
                pitchVal = int(abs(100 - RHnormalX) ** 1.5)
                volumeVal = 400 - LHnormalY

                if volumeVal > 100:
                    volumeVal = 100
                if volumeVal < 0:
                    volumeVal = 0
                tmn.set_freq(pitchVal)

    pygame.display.flip()