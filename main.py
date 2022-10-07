from skeletonGen import skeleton
from configparser import ConfigParser
from muscleGen import muscle
import json
from uIdGen import uId
import json
import codecs
import os
import glob
import shutil
import platform

userOS = platform.system()
print(userOS)
if userOS == 'Darwin':
	dirDivide = '/'
elif userOS == 'Windows':
	dirDivide = "\\"
else:
	print('Invalid operating system\n\nSorry!')
	

print('\n\n****Blender MB-Lab Character Generator****\n\n')
print('Generates JSON data that you can import into MB-Lab add-on for Blender\n')
print('Please see the README for more details, thank you\n\n')
print('Jefferson Haadsma 2022\n\n')

#reads data from config.ini
config_object = ConfigParser()
config_object.read('.' + dirDivide + "config.ini")

#Lists available character configurations, then asks user to choose a configuration, chosen configuration is used 
print('\n\nWhat type of Characters would you like to generate. Enter choice from below, or press enter for DEFAULT configuration')
print(config_object.sections())
configChoice = input()

if configChoice == '':
	configChoice = 'MB'
typeOfHuman = config_object[configChoice]

print('\n\nInput how many characters you would like to generate:')

#number of characteres to be generated
charNum = int(input())

#Limits number of character generated at once as to not take up too much user data accidently
#Plan to update to read amount of storage on user system and base limit on that
if charNum >=1000:
	charNum = 1000

#improve naming convention for less confusion (ie fAvg and faAvg etc)
#convert to doubles(decimal)

#converts config data into variables used by the construction funtions
hAvg = float(typeOfHuman["body_height_Z"])
hStdDev = float(typeOfHuman["height_std_dev"])
fAvg = float(typeOfHuman["upperleg_length"])
tiAvg = float(typeOfHuman["lowerleg_length"])
ftAvg = float(typeOfHuman["feet_height_Z"])
heAvg = float(typeOfHuman["head_height_Z"])
toAvg = float(typeOfHuman["torso_height_Z"])
nAvg = float(typeOfHuman["neck_height_Z"])
hiAvg = float(typeOfHuman["buttock_height_Z"])
wAvg = float(typeOfHuman["wingspanAvg"])
wStdDev = float(typeOfHuman["wingspanStdDev"])
sAvg = float(typeOfHuman["shoulders_width"])
haAvg = float(typeOfHuman["hands_length"])
faAvg = float(typeOfHuman["forearm_length"])
huAvg = float(typeOfHuman["upperarm_length"])
hipBAvg = float(typeOfHuman["buttock_width_X"]) ####
ankleCAvg = float(typeOfHuman["ankleCircAvg"])###
wristCAvg = float(typeOfHuman["wrist_girth"])###
chestWAvg = float(typeOfHuman["chest_width"])
chestGAvg = float(typeOfHuman["chest_girth"])
neckGAvg = float(typeOfHuman["neck_girth"])
waistGAvg = float(typeOfHuman["waist_girth"])
buttockGAvg = float(typeOfHuman["buttock_girth"])

bMscleAvg = float(typeOfHuman["baseMuscleAvg"])
bMscleStd = float(typeOfHuman["baseMuscleStdDev"])
expEndAvg = float(typeOfHuman["expEndRatioAvg"])
expEndStd = float(typeOfHuman["expEndRatioStdDev"])

eType = typeOfHuman["type"]


# Checks if storage directory exits in CWD, if it does not exist it creates one named 'storage'
storage_dir = 'storage'
cwd = os.getcwd()
dir_list = os.listdir(cwd)
create_storage_dir =  cwd + dirDivide +  storage_dir 
for s in dir_list:
	if storage_dir in dir_list:
		print("\nFolder Exists\n")
		print(create_storage_dir)
		break
	else:
		print("\nCreating folder\n")
		os.mkdir(create_storage_dir)
		break

dir_path = create_storage_dir + dirDivide

#Prompts user to choose to save character or not
print('Create new, enter "1"')
print('Add to existing, enter "2"')
saveC = input()


#User chooses number of characters
#Character(s) stats stored in one text file, and individual json files per character
#json file named the uid of the character
#files stored in generated directory that is the same name as text file that user chooses

#If user chooses option 2, create new file
if saveC == '1':
	
	#Prompts user to choose name for file and folder
	print('Enter what you would like to name your file/folder')
	fileDirName = input()
	#Creates subdirectory inside 'storage' directory
	os.mkdir(dir_path + fileDirName)
	new_dir = dir_path + fileDirName + '/'
	use_dir = new_dir
	os.mkdir(new_dir + 'json')
	jsonDir = new_dir + 'json/'
	#Creates .txt file inside newly created directory
	newTextFile = new_dir +  fileDirName + '.txt'
	f = open(newTextFile, "w+")
	textFile = newTextFile

	total, used, free = shutil.disk_usage(__file__)
	print(total, used, free)
	


elif saveC == '2':
		
	print("Enter a directory from the list:\n\n")
	print(os.listdir(dir_path))
	chooseDir = input()
	use_dir = dir_path + chooseDir + '/'
	textFile = use_dir + chooseDir + '.txt'
	jsonDir = use_dir + 'json/'


#Following creates the characters
for k in range (charNum):
	testHumanSkel = skeleton( hAvg, hStdDev, fAvg, tiAvg, ftAvg, heAvg, toAvg, nAvg, hiAvg, wAvg, wStdDev, sAvg, haAvg, faAvg, huAvg, hipBAvg, ankleCAvg, wristCAvg, chestWAvg, chestGAvg, neckGAvg, waistGAvg, buttockGAvg)
	testHumanId = uId()
	testHumanMuscle = muscle(bMscleAvg, bMscleStd, expEndAvg, expEndStd)


	#Create new formatting variable for json
	#Formatted string variable for text and json storage, not final, in progress
	tHumanTxt = ["\n\n{\n\nID: ", str(testHumanId),
			"\nType:", eType, 
			"\n\nHeight: ", str(testHumanSkel.outputHeight), 
			"\nWinspan: ", str(testHumanSkel.wingspan), 
			"\nUpper Leg Length: ", str(testHumanSkel.upperLegLength), 
			"\nLower Leg Length", str(testHumanSkel.lowerLegLength),
			"\nFoot Height: ", str(testHumanSkel.footHeight),
			"\nHead Height: ", str(testHumanSkel.headHeight),
			"\nTorso Height: ", str(testHumanSkel.torsoHeight),
			"\nNeck Height: ", str(testHumanSkel.neckHeight),
			"\nHip Height: ", str(testHumanSkel.hipHeight),
			"\nShoulder Width: ", str(testHumanSkel.shoulderWidth),
			"\nHand length: ", str(testHumanSkel.handLength),
			"\nForearm length: ", str(testHumanSkel.forearmLength),
			"\nHumerus Length: ", str(testHumanSkel.upperArmLength), 
			"\n\nHip breadth:", str(testHumanSkel.hipWidth), 
			"\n\nAnkle Circumference:", str(testHumanSkel.ankleCirc), 
			"\nWrist Circumference:", str(testHumanSkel.wristCirc), 
			"\nChest Width:", str(testHumanSkel.chestWidth),
			"\nChest Girth:", str(testHumanSkel.chestGirth),
			"\nNeck Girth:", str(testHumanSkel.neckGirth),
			"\nWaist Girth:", str(testHumanSkel.waistGirth),
			"\nButtock Girth:", str(testHumanSkel.buttockGirth),
			"\n\nBaseline Muscle:", str(testHumanMuscle.baselineMuscle), 
			"\nExplosive to Endurance muscle ratio:", str(testHumanMuscle.explosiveEnduranceRatio), "\n\n}"]
			#needs major formatting
	
	#Writes data into text file
	with open(textFile, 'a') as f:
		for line in tHumanTxt:
			f.write(line)



	def jsonFormat(humanVar):
		jsonVar = float(humanVar) * .01
		return jsonVar

	jsonHeight = jsonFormat(testHumanSkel.outputHeight)
	jsonUpperLegLength = jsonFormat(testHumanSkel.upperLegLength)
	jsonLowerLegLength = jsonFormat(testHumanSkel.lowerLegLength)
	jsonFootHeight = jsonFormat(testHumanSkel.footHeight)
	jsonHeadHeight = jsonFormat(testHumanSkel.headHeight)
	jsonTorsoHeight = jsonFormat(testHumanSkel.torsoHeight)
	jsonNeckHeight = jsonFormat(testHumanSkel.neckHeight)
	jsonHipHeight = jsonFormat(testHumanSkel.hipHeight)
	jsonShoulderWidth = jsonFormat(testHumanSkel.shoulderWidth)
	jsonHandLength = jsonFormat(testHumanSkel.handLength) 
	jsonForearmLength = jsonFormat(testHumanSkel.forearmLength) 
	jsonUpperArmLength = jsonFormat(testHumanSkel.upperArmLength) 
	jsonHipBreadth = jsonFormat(testHumanSkel.hipWidth)
	jsonAnkleCirc = jsonFormat(testHumanSkel.ankleCirc)
	jsonWristCirc = jsonFormat(testHumanSkel.wristCirc)
	jsonChestWidth = jsonFormat(testHumanSkel.chestWidth)
	jsonChestGirth = jsonFormat(testHumanSkel.chestGirth)
	jsonNeckGirth = jsonFormat(testHumanSkel.neckGirth)
	jsonWaistGirth = jsonFormat(testHumanSkel.waistGirth)
	jsonButtockGirth = jsonFormat(testHumanSkel.buttockGirth)

	#store all these values in an array, then cycle through them?


	#Formatted for MBlab JSON data
	tHumanJson =  {"manuellab_vers": [1, 7, 7], "measures": {"upperleg_length": jsonUpperLegLength, "buttock_depth_Y": .255 , "chest_girth": jsonChestGirth, "wrist_girth": jsonWristCirc, "upperarm_axillary_girth": 0.368, "neck_girth": jsonNeckGirth, "lowerleg_length": jsonLowerLegLength, "lowerleg_bottom_girth": 0.216, "head_height_Z": jsonHeadHeight, "feet_length": 0.284, "lowerleg_calf_girth": 0.397, "feet_heel_width": 0.078, "torso_height_Z": jsonTorsoHeight, "upperleg_top_girth": 0.569, "shoulders_width": jsonShoulderWidth, "feet_height_Z": jsonFootHeight, "buttock_width_X": jsonHipBreadth, "waist_girth": jsonWaistGirth, "elbow_girth": 0.307, "head_width_X": 0.151, "chest_depth_Y": 0.244, "upperleg_bottom_girth": 0.436, "forearm_length": jsonForearmLength, "buttock_height_Z": jsonHipHeight, "hands_width": 0.088, "hands_length": jsonHandLength, "upperarm_length": jsonUpperArmLength, "feet_width": 0.109, "body_height_Z": jsonHeight, "neck_height_Z": jsonNeckHeight, "head_length": 0.215, "buttock_girth": jsonButtockGirth, "chest_width_X": jsonChestWidth}}
	
	#stores generated variable values into above json string
	jsonFileName = jsonDir + testHumanId + '.json'
	e = open(jsonFileName, "w+")
	with open(jsonFileName, "a") as j:
		json.dump(tHumanJson,j)			
	

	



	
