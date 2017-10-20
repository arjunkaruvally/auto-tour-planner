( define (problem problem1)
    (:domain
        travel-domain    
    )
    (:objects
        waypoint1
        user1
    )
    
    (:init
        (= (total-score) 0)
        (user user1)
		
		(waypoint waypoint1)
		(= (score waypoint1) 30)
		(not ( visited user1 waypoint1) )
	)

	(:goal
		(and
			(visited user1 waypoint1)
    	)
    )
    (:metric 
        maximize (total-score)
    )
)
