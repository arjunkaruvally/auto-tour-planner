
(define (problem problem)
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
        (= (end-time) 20)
        (user user1)
		(waypoint waypoint1)
		(= (score waypoint1) score)
		(= (duration waypoint1) duration)
		(waypoint waypoint2)
		(= (score waypoint2) 10)
		(= (duration waypoint2) 1)
		(waypoint waypoint3)
		(= (score waypoint3) 20)
		(= (duration waypoint3) 2)
		(waypoint waypoint4)
		(= (score waypoint4) 30)
		(= (duration waypoint4) 2)
		(not ( visited user1 waypoint1) )
		(not ( visited user1 waypoint2) )
		(not ( visited user1 waypoint3) )
		(not ( visited user1 waypoint4) )
		(user-at user1 waypoint1) ) 

	(:goal
		(and
			(visited user1 waypoint1)
			(visited user1 waypoint2)
			(visited user1 waypoint3)
			(visited user1 waypoint4)

    	)
    )
    (:metric 
        maximize (total-score)         
    )
)

