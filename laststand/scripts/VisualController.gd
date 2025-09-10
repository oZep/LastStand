extends Node

# References to your visual nodes (sprites or 3D models).
# You will set these up in the scene editor later.
onready var mac_visuals = get_node("../Mac/AnimatedSprite3D")
onready var player_visuals = get_node("../Player/AnimatedSprite3D")

# A dictionary to map actions to animation names.
var anim_map = {
	"stand": "standing_anim",
	"duck": "ducking_anim",
	"shoot": "shooting_anim"
}

func play_turn_visuals(player_action, mac_action):
	# Determine the visual priority based on your rules.
	# The 'both shoot' condition is a unique case.
	if player_action == "shoot" and mac_action == "shoot":
		play_both_shoot_visuals()
		return

	# Check for Mac's action first, then the player's.
	if mac_action == "stand":
		# Play Mac's standing animation first.
		mac_visuals.play(anim_map["stand"])
		# Wait for the animation to finish, then play the player's.
		yield(mac_visuals, "animation_finished")
		player_visuals.play(anim_map[player_action])
		yield(player_visuals, "animation_finished")
		
	elif mac_action == "duck":
		mac_visuals.play(anim_map["duck"])
		yield(mac_visuals, "animation_finished")
		player_visuals.play(anim_map[player_action])
		yield(player_visuals, "animation_finished")
		
	elif mac_action == "shoot":
		mac_visuals.play(anim_map["shoot"])
		yield(mac_visuals, "animation_finished")
		player_visuals.play(anim_map[player_action])
		yield(player_visuals, "animation_finished")

	print("Animations completed. Proceeding to next step.")

func play_both_shoot_visuals():
	# This is where your unique animation for a simultaneous shot will play.
	# For now, let's just make both shoot at the same time.
	player_visuals.play("both_shoot_anim")
	mac_visuals.play("both_shoot_anim")
	print("Both players shot at the same time!")
