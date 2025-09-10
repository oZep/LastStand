extends Node

var player_bullets = 3
var mac_bullets = 3
var player_action = ""
var mac_action = ""
var round_active = false
var visual_controller = null

func _ready():
	# Get a reference to the VisualController node.
	visual_controller = get_node("VisualController")
	start_new_round()

func start_new_round():
	round_active = true
	# For now, let's just make Mac choose a random action.
	var mac_choices = ["stand", "duck", "shoot"]
	mac_action = mac_choices[randi() % mac_choices.size()]
	
	print("New round started. Choose your action: 'stand', 'duck', or 'shoot'.")
	print("Mac has chosen: ", mac_action)

func take_turn(player_choice):
	if not round_active:
		return
	
	player_action = player_choice
	
	# Check if a bullet was used and deduct it.
	if player_action == "shoot":
		player_bullets -= 1
	if mac_action == "shoot":
		mac_bullets -= 1
		
	# Now, pass the actions to the visual controller for playback.
	visual_controller.play_turn_visuals(player_action, mac_action)
	
	# After animations are done, we will check for win conditions.
	# For a simple test, we will just start a new round.
	round_active = false
	call_deferred("start_new_round")
