( define (problem problem1)
    (:domain
        travel-domain    
    )
    (:objects
        waypoint1 waypoint2 waypoint3
        user1
    )
    
    (:init
        (= (total-score) 0)
        (= (current-time) 10)
        (= (end-time) 18)
        (user user1)
		
		(waypoint waypoint2)
		(= (score waypoint2) 10)
		(= (duration waypoint2) 1)
		(waypoint waypoint3)
		(= (score waypoint3) 20)
		(= (duration waypoint3) 2)
		(waypoint waypoint1)
		(= (score waypoint1) 30)
		(= (duration waypoint1) 2)
		(not ( visited user1 waypoint1) )
		(not ( visited user1 waypoint2) )
		(not ( visited user1 waypoint3) )
		
		(= (drive-time waypoint1 waypoint3) 2 )
		(= (drive-time waypoint3 waypoint1) 2 )
		
		(= (drive-time waypoint1 waypoint2) 5 )
		(= (drive-time waypoint2 waypoint1) 5 )
		
		(= (drive-time waypoint3 waypoint2) 2 )
		(= (drive-time waypoint2 waypoint3) 2 )

		(user-at user1 waypoint1)
	)

	(:goal
		(and
			(visited user1 waypoint1)
			(visited user1 waypoint2)
			(visited user1 waypoint3)
    	)
    )
    (:metric 
        maximize (total-score)
    )
)
