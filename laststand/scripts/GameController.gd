extends Node

var player_bullets = 3
var mac_bullets = 3
var player_action = ""
var mac_action = ""
var round_active = false
var visual_controller = null
var player_stuck = false
var mac_stuck = false

func _ready():
	# Get a reference to the VisualController node.
	visual_controller = get_node("VisualController")
	start_new_round()

func start_new_round():
	round_active = true
	# Mac's action for this round.
	var mac_choices = ["stand", "duck", "shoot"]
	
	# i have to adjust this logic TODO: Make mac smart
	mac_action = mac_choices[randi() % mac_choices.size()]
	
	if mac_stuck:
		mac_action = "stuck"
		mac_stuck = false
		
	print("New round started. Choose your action: 'stand', 'duck', or 'shoot'.")
	print("Mac's action for this round: ", mac_action)

func take_turn(player_choice):
	if not round_active:
		return
	
	player_action = player_choice
	
	if player_stuck:
		player_action = "stuck"
		player_stuck = false
	
	# Check if a bullet was used and deduct it.
	if player_action == "shoot":
		player_bullets -= 1
	if mac_action == "shoot":
		mac_bullets -= 1
		
	# Now, pass the actions to the visual controller for playback.
	visual_controller.play_turn_visuals(player_action, mac_action)
	
	# Check for the lasso condition based on the previous round's actions.
	if player_choice == "stand" and mac_action != "shoot" and mac_action != "duck":
		mac_stuck = true
		
	if mac_action == "stand" and player_choice != "shoot" and player_choice != "duck":
		player_stuck = true
	
	# After animations are done, we will check for win conditions.
	# For a simple test, we will just start a new round.
	round_active = false
	call_deferred("start_new_round")
