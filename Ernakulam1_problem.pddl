
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
		(= (score waypoint1) 2.0)
		(= (duration waypoint1) 2)
		(waypoint waypoint2)
		(= (score waypoint2) 2.33333333333)
		(= (duration waypoint2) 2)
		(waypoint waypoint3)
		(= (score waypoint3) 1.83333333333)
		(= (duration waypoint3) 2)
		(waypoint waypoint4)
		(= (score waypoint4) 2.5)
		(= (duration waypoint4) 2)
		(waypoint waypoint5)
		(= (score waypoint5) 2.35714285714)
		(= (duration waypoint5) 2)
		(waypoint waypoint6)
		(= (score waypoint6) 2.0)
		(= (duration waypoint6) 2)
		(waypoint waypoint7)
		(= (score waypoint7) 2.25)
		(= (duration waypoint7) 2)
		(waypoint waypoint8)
		(= (score waypoint8) 1.73333333333)
		(= (duration waypoint8) 2)
		(waypoint waypoint9)
		(= (score waypoint9) 2.45255474453)
		(= (duration waypoint9) 2)
		(waypoint waypoint10)
		(= (score waypoint10) 0.0)
		(= (duration waypoint10) 2)
		(waypoint waypoint11)
		(= (score waypoint11) 2.0)
		(= (duration waypoint11) 2)

    	)
    )
    (:metric 
        maximize (total-score)         
    )
)
