pose_to_use = 'Psi'


from openni import *
import math, pygame, SimpleCV
import time
import accordian, guitar
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


# Create the user generator
user = UserGenerator()
user.create(ctx)

# Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap

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
    if status == CALIBRATION_STATUS_OK:
        print "4/4 User {} calibrated successfully! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)

def lost_user(src, id):
    print "--- User {} lost." .format(id)
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

# Return true if line segments AB and CD intersect
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
olds = [(0,0), (0,0), (0,0), (0,0), (0,0)]
dist = 0
i = 0
slope = 0
oldX, oldY = 0,0 
t = time.time()
chords = 0
dist = 0
while True:
    # Update to next frame
    ctx.wait_and_update_all()
    image = kinectImage.get_raw_image_map_bgr()
    newImage = pygame.image.fromstring(image,(640,480),"RGB")
    finalImage = SimpleCV.Image(pygame.surfarray.array2d(newImage)).flipHorizontal()
    
    finalImage.save('asd.png')
    finalImage = pygame.image.load('asd.png')
    screen.blit(finalImage,(0,0))


    if instrument == 'accordian':
        font=pygame.font.Font(None,30)
        # scoretext=font.render("Slope:"+str(slope), 1,(255,255,255))

        if i == 0:
            scoretext=font.render("DECRESING:", 1,(255,255,255))
        elif i == 1:
            scoretext=font.render("SAME:", 1,(255,255,255))
        else:
            scoretext=font.render("INCREASING:", 1,(255,255,255))
    if instrument == 'violin':
        font=pygame.font.Font(None,30)

        slopetext=font.render(str(slope), 1,(255,255,255))
        
        screen.blit(slopetext, (500, 457))
    if instrument == 'guitar':
        font=pygame.font.Font(None,30)

        slopetext=font.render("CHORDS: " + str(chords), 1,(255,255,255))
        if dist <60:
            disttext=font.render("NONE: " + str(dist), 1,(255,255,255))
        elif dist < 132:
            disttext=font.render("C0: " + str(dist), 1,(255,255,255))
        elif dist < 204:
            disttext=font.render("C1: " + str(dist), 1,(255,255,255))
        elif dist < 276:
            disttext=font.render("C2: " + str(dist), 1,(255,255,255))
        elif dist < 348:
            disttext=font.render("C3: " + str(dist), 1,(255,255,255))
        else:
            disttext=font.render("C4: " + str(dist), 1,(255,255,255))
        screen.blit(slopetext, (500, 457))
        screen.blit(disttext, (0, 457))

    # Extract head position of each tracked user
    # if instrument == 'drum':
    #     d1 = [(100,100),(200,100)]
    #     d2 = [(200,200),(300,200)]
    #     drums = [d1, d2]

    #     for drum in drums:
    #         print "WE GOTSA DRUM"
    #         pygame.draw.line(screen, (0,0,255), drum[0],drum[1], 1)

    for id in user.users:
        if skel_cap.is_tracking(id):
            t1 = time.time()
            RH = skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
            LH = skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
            #determine key point for instrument
            if instrument == 'accordian':
                KP = skel_cap.get_joint_position(id, SKEL_NECK)  #dont need this
                KP = KP.point
            elif instrument == 'guitar':
                KP1 = skel_cap.get_joint_position(id, SKEL_RIGHT_HIP)
                KP2 = skel_cap.get_joint_position(id, SKEL_LEFT_HIP)

                KP = [(KP1.point[x]+KP2.point[x])/2 for x in range(3)]
                KP = KP2.point
            elif instrument == 'violin':
                KP = skel_cap.get_joint_position(id, SKEL_NECK).point
            elif instrument == 'drum':
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
                tmpD = (LHnormalX - RHnormalX)
                if tmpD > dist + 5:
                    accordian.play("in")
                    i = 2
                elif tmpD < dist - 5:
                    i = 0
                    accordian.play("out")
                else:
                    i = 1
                    accordian.stop()
                dist = tmpD
            if instrument == 'guitar':
                slope = (KPnormalY-RHnormalY)/(RHnormalX-KPnormalY)
                pygame.draw.line(screen, (0,255,0), (RHnormalX, RHnormalY),(KPnormalX,KPnormalY), 1)
                dist = ((KPnormalY-RHnormalY)**2+(RHnormalX-KPnormalY)**2)**.5
               
                if intersect([LHnormalX, LHnormalY], [oldX,oldY], [RHnormalX, RHnormalY], [KPnormalX, KPnormalY]):
                    chords += 1
                    
                    guitar.stop()
                    #dist 60-400
                    if dist <30:
                        pass
                    elif dist < 102:
                        guitar.play(4)
                    elif dist < 174:
                        guitar.play(3)
                    elif dist < 246:
                        guitar.play(2)
                    elif dist < 318:
                        guitar.play(1)
                    else:
                        guitar.play(0)
                pygame.draw.line(screen, (0,255,0), (oldX, oldY),(LHnormalX,LHnormalY), 1)
                if time.time() - t > .1:
                    oldX = LHnormalX
                    oldY = LHnormalY
                    t = time.time()
            if instrument == 'drum':
                d1 = [(100,-50),(200,-50)]
                d2 = [(0,-20),(100,-20)]
                d3 = [(-100,-50),(-200,-50)]

                drums = [d1, d2, d3]

                for drum in drums:

                    pygame.draw.line(screen, (255,0,0), add(KPNORMAL[:2],drum[0]),add(KPNORMAL[:2],drum[1]), 5)

            if instrument == 'violin':
                # pygame.draw.line(screen, (0,255,0), (RHnormalX, RHnormalY),(KPnormalX,KPnormalY), 1)
                if time.time() - t > .1:
                    try:
                        slope = (KPnormalY-oldY)/(RHnormalX-oldX)
                    except:
                        slope = 0
                    t = time.time()
                oldX, oldY = RHnormalX, RHnormalY
                p1 = [KPnormalX, KPnormalY]
                p2 = [RHnormalX, RHnormalY]


                pygame.draw.line(screen, (0,255,0), p1, p2, 3)

                #draw the bow


    pygame.display.flip()