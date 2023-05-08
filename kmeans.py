import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def create_text_render(string, color):
	font = pygame.font.SysFont('sans', 40)
	return font.render(string, True, color)
def distance(p1, p2):
	return math.sqrt( ((p1[0] - p2[0])*(p1[0] - p2[0])) + ((p1[1] - p2[1])*(p1[1] - p2[1])) )

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("Kmeans Visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214,214,214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249,255,230)
WHITE = (255,255,255)
font_small = pygame.font.SysFont('sans', 20)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

text_plus = create_text_render("+",WHITE)
text_minus = create_text_render("-",WHITE)
text_run = create_text_render("Run",WHITE)
text_random = create_text_render("Random ",WHITE)
text_algorithm = create_text_render("Algorithm",WHITE)
text_reset = create_text_render("Reset",WHITE)	


K = 0
error = 0
points = []
clusters = []
labels = []
while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	#Draw Interface
	#Draw Panel
	pygame.draw.rect(screen, BLACK, (50,50,700,500))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))

	#K button +
	pygame.draw.rect(screen, BLACK, (850,50,50,50))
	screen.blit(text_plus, (860,50))
	#K button -
	pygame.draw.rect(screen, BLACK, (950,50,50,50))
	screen.blit(text_minus, (960,50))

	#Text K
	text_k = create_text_render("K = ",BLACK)
	screen.blit(text_k, (1050,50))
	text_numof_k = create_text_render(str(K),BLACK)
	screen.blit(text_numof_k, (1120,50))

	# Run button
	pygame.draw.rect(screen, BLACK, (850,150,150,50))
	screen.blit(text_run, (890,150))

	# Random button
	pygame.draw.rect(screen, BLACK, (850,250,160,50))
	screen.blit(text_random, (850,250))

	# Reset button
	pygame.draw.rect(screen, BLACK, (850,550,150,50))
	screen.blit(text_reset, (870,550))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (850,450,180,50))
	screen.blit(text_algorithm, (850,450))

	#Text Error
	text_error = create_text_render("Error = ",BLACK)
	screen.blit(text_error, (850,350))
	text_numof_erro = create_text_render(str(error),BLACK)
	screen.blit(text_numof_erro, (1000,350))
	#End draw Interface

	#Draw mouse position
	if (55 < mouse_x < 745) and (55 < mouse_y < 545):
		text_mouse = font_small.render("(" + str(mouse_x - 55) + ", " + str(mouse_y - 55) + ")", True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y + 10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			#create point on panel
			if (55 < mouse_x < 745) and (55 < mouse_y < 545):
				labels = []
				point = [mouse_x - 55, mouse_y - 55]
				points.append(point)
			#Change K button +
			if (850 < mouse_x < 900) and (50 < mouse_y < 100):
				K = K + 1
				if K > 9:
					print("The system only accepts K less than or equal to 9")
					K = 9
			#Change K button -
			if (950 < mouse_x < 1000) and (50 < mouse_y < 100):
				if K > 0:
					K = K - 1
				print("Press K-")
			#Run Button
			if (850 < mouse_x < 1000) and (150 < mouse_y < 200):
				labels = []
				if clusters == []:
					continue
				#Assign points to closet clusters
				for p in points:
					distances_to_clusters = []
					for c in clusters:
						dis = distance(p,c)
						distances_to_clusters.append(dis)
					min_distance = min(distances_to_clusters)
					label = distances_to_clusters.index(min_distance)
					labels.append(label)

				#Update clusters
				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x = sum_x + points[j][0]
							sum_y = sum_y + points[j][1]
							count = count + 1
					if count != 0:
						new_cluters_x = sum_x/count
						new_cluters_y = sum_y/count
						clusters[i] = [new_cluters_x, new_cluters_y]

			#Random Button
			if (850 < mouse_x < 1010) and (250 < mouse_y < 300):
				labels = []
				clusters = []
				for i in range(K):
					random_point = [randint(0,700), randint(0,500)]
					clusters.append(random_point)
			#Reset Button
			if (850 < mouse_x < 1000) and (550 < mouse_y < 600):
				points = []
				labels = []
				clusters = []
				error = 0
				K = 0
			#Algorithm Button
			if (850 < mouse_x < 1030) and (450 < mouse_y < 500):
				try:
					kmeans = KMeans(n_clusters=K).fit(points)
					labels = kmeans.predict(points)
					clusters = kmeans.cluster_centers_
				except:
					print("Error!!!!!. You need to add points")
	#Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) +55, int(clusters[i][1]) +55), 10)


	#Draw points
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0] +55, points[i][1] +55), 6)
		if labels == []:
			pygame.draw.circle(screen, WHITE, (points[i][0] +55, points[i][1] +55), 5)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] +55, points[i][1] +55), 5)


	#Calculate and draw error
	error = 0
	for i in range(len(points)):
		if clusters != [] and labels != []:
			error = error + int(distance(points[i], clusters[labels[i]]))
	text_numof_erro = create_text_render(str(error),BLACK)
	screen.blit(text_numof_erro, (1000,350))	

	pygame.display.flip()

pygame.quit()







