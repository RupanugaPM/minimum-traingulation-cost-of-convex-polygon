import pygame, sys, random , time
import math

width=800
height=800

clock = pygame.time.Clock()
pygame.init() # initiates pygame
pygame.display.set_caption('Convex Polygon Triangulation')
WINDOW_SIZE = (width,height)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

def orientation(p, q, r):
    '''
    To find orientation of ordered triplet (p, q, r). 
    The function returns following values 
    0 --> p, q and r are collinear 
    >0 --> Clockwise 
    <0 --> Counterclockwise 
    '''
    val = (q[1] - p[1]) * (r[0]- q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return val  
def convexHull(points):
    n=len(points)
    # There must be at least 3 points 
    if n < 3:
        return []
    # Find the leftmost point
    l = 0
    for i in range(1,len(points)):
        if points[i][0] < points[l][0]:
            l = i
        elif points[i][0] == points[l][0]:
            if points[i][1] > points[l][1]:
                l = i
  
    hull = []
      
    '''
    Start from leftmost point, keep moving counterclockwise 
    until reach the start point again. This loop runs O(h) 
    times where h is number of points in result or output. 
    '''
    p = l
    q = 0
    while(True):
          
        # Add current point to result 
        hull.append(p)
  
        '''
        Search for a point 'q' such that orientation(p, q, 
        x) is counterclockwise for all points 'x'. The idea 
        is to keep track of last visited most counterclock- 
        wise point in q. If any point 'i' is more counterclock- 
        wise than q, then update q. 
        '''
        q = (p + 1) % n
  
        for i in range(n):
              
            # If i is more counterclockwise 
            # than current q, then update q 
            if(orientation(points[p], points[i], points[q]) <0):
                q = i
  
        '''
        Now q is the most counterclockwise with respect to p 
        Set p as q for next iteration, so that q is added to 
        result 'hull' 
        '''
        p = q
  
        # While we don't come to first point
        if(p == l):
            break
  
    # Set it in Answer
    ans=[]
    for each in hull:
        ans.append((points[each][0], points[each][1]))
    return ans

def dist(p1,  p2):
    #distance between 2 points
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))
def cost(p1,p2,p3):
    #cost of the function can be changed to area of triangle/ other things
    return dist(p1, p2) + dist(p2, p3) + dist(p3, p1)
def triangulation(points):
    # There must be at least 3 points
    n=len(points)
    if (n < 3):
        return []
    # table[i][j] stores cost of triangulation from i to j
    # also the index which made it minimum
    table = [[0.0,-1] * (n) for _ in range(n)]
    for gap in range(n):
        for j in range(gap,n):
            i=j-gap
            if (j < i + 2):
                table[i][j] = [0.0,-1]
            else:
                table[i][j] = [1000000000000.0,-1]
                for k in range(i+1,j):
                    val = table[i][k][0] + table[k][j][0] +cost(points[i], points[j], points[k])
                    if (table[i][j][0] > val):
                        table[i][j] = [val,k]
    #now we return all the the triangles formed
    queue=[[0,n-1]]
    triangles=[]
    while len(queue)>0:
        x=queue.pop(0)
        k=table[x[0]][x[1]][1] # get the index which is minimising
        #push to queue if polygon has atleast 3 sides
        if k-x[0]>2:
            queue.append([x[0],k])
        if x[1]-k>2:
            queue.append([k,x[1]])
        #push the triangle to triangles
        triangles.append([points[x[0]],points[k],points[x[1]]])
    return triangles
        
#Dictionary of points so that no repeated 
pd={}

polygonp=[]
triangles=[]
triangle_color=[]

t1=time.time()
t2=time.time()

while True: # game loop
    screen.fill((0,0,0))
    #mx, my = pygame.mouse.get_pos()
    #spd=pygame.mouse.get_pos()[0]/16

    if(len(polygonp)>2):
        pygame.draw.polygon(screen,(255,255,255),polygonp)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    #moving charecter
    if keys[pygame.K_a]:
        #position of mouse to be added to dictionary of points
        mpos=tuple(pygame.mouse.get_pos())
        pd[mpos]=1
        points=[]
        for i in pd:
            points.append(i)
        polygonp=convexHull(points)
        triangles=triangulation(polygonp)
        triangle_color=[]
        for i in range(len(triangles)):
            triangle_color.append([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
    if keys[pygame.K_s]:
        for i in range(len(triangles)):
            pygame.draw.polygon(screen,triangle_color[i],triangles[i])
    if keys[pygame.K_c]:
        pd={}
        triangles=[]
        triangle_color=[]
        polygonp=[]
        
    pygame.display.update()
    clock.tick(60)

