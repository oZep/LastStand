extends Node2D

@export var animation_player: AnimatedSprite2D

func play_intro():
	var bullets_to_load = 2
	
	for i in range(1):
		animation_player.play("LoadBullets1_anim")
		await animation_player.animation_finished
		
		# gotta use the AnimationPlayer :( 
	
func _ready():
	play_intro()
