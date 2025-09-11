extends Node

# References to your visual nodes (sprites or 3D models).
# You will set these up in the scene editor later.
onready var mac_visuals = get_node("../Mac/AnimatedSprite3D")
onready var player_visuals = get_node("../Player/AnimatedSprite3D")

# A dictionary to map actions to animation names.
var anim_map = {
	"stand": "standing_anim",
	"duck": "ducking_anim",
	"shoot": "shooting_anim",
	"stuck": "stuck_anim"
}

func play_turn_visuals(player_action, mac_action):
	# This is where your custom logic for each combination will go.
	# The visualization you provided is extremely helpful for this.
	
	# Mac priority for "Shoot" and "Stuck"
	if mac_action == "stuck":
		# Mac is stuck, so only the player can perform an action.
		mac_visuals.play(anim_map["stuck"])
		yield(mac_visuals, "animation_finished")
		player_visuals.play(anim_map[player_action])
		yield(player_visuals, "animation_finished")
	elif mac_action == "shoot":
		# Special handling for Mac's "Shoot" action.
		if player_action == "duck":
			# Mac shoots, player ducks.
			mac_visuals.play(anim_map["shoot"])
			yield(mac_visuals, "animation_finished")
			player_visuals.play(anim_map["duck"])
			yield(player_visuals, "animation_finished")
		elif player_action == "stand":
			# Mac shoots, player stands (gets hit).
			mac_visuals.play(anim_map["shoot"])
			yield(mac_visuals, "animation_finished")
			player_visuals.play("defeat_anim")
			yield(player_visuals, "animation_finished")
		else:
			# Both players shoot at the same time.
			play_both_shoot_visuals()
	# Player's turn to have priority.
	elif player_action == "shoot":
		# Player shoots, Mac takes a non-shoot action.
		if mac_action == "duck":
			# Player shoots, Mac ducks.
			player_visuals.play(anim_map["shoot"])
			yield(player_visuals, "animation_finished")
			mac_visuals.play(anim_map["duck"])
			yield(mac_visuals, "animation_finished")
		elif mac_action == "stand":
			# Player shoots, Mac stands (gets hit).
			player_visuals.play(anim_map["shoot"])
			yield(player_visuals, "animation_finished")
			mac_visuals.play("defeat_anim")
			yield(mac_visuals, "animation_finished")
	# Remaining combinations where neither player shoots.
	elif mac_action == "stand":
		if player_action == "duck":
			# Mac stands, player ducks.
			mac_visuals.play(anim_map["stand"])
			yield(mac_visuals, "animation_finished")
			player_visuals.play(anim_map["duck"])
			yield(player_visuals, "animation_finished")
		elif player_action == "stand":
			# Mac and player stand. This results in Mac getting stuck next turn.
			mac_visuals.play(anim_map["stand"])
			yield(mac_visuals, "animation_finished")
			player_visuals.play(anim_map["stand"])
			yield(player_visuals, "animation_finished")
	elif mac_action == "duck":
		# Mac ducks, player takes a non-shoot action.
		mac_visuals.play(anim_map["duck"])
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
