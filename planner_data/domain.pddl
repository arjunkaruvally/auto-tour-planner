(define (domain travel-domain)
    (:requirements :fluents )

    (:predicates
        (user  ?user)
        (waypoint ?poi)
        (visited ?user ?poi)
        (user-at ?user ?poi)
    )
    (:functions
        (score ?poi) 
        (total-score)
        (current-time)
        (end-time)
        (duration ?poi)
        (drive-time ?from-poi ?to-poi)
    )

    (:action visit-penalised
        :parameters 
            (?user
             ?poi)

        :precondition 
            (and 
                (user-at ?user ?poi)
                ( not (visited ?user ?poi) )
                (>= (current-time) (end-time))
            )

        :effect 
            (and 
                (visited ?user ?poi)
                ( decrease (total-score) (score ?poi) )
                ( increase (current-time) (duration ?poi))
            )
    )
    (:action visit
        :parameters 
            (?user
             ?poi)

        :precondition 
            (and 
                (user-at ?user ?poi)
                ( not (visited ?user ?poi) )
                (< (current-time) (end-time))
            )

        :effect 
            (and 
                (visited ?user ?poi)
                ( increase (total-score) (score ?poi) )
                ( increase (current-time) (duration ?poi))
            )
    )
    (:action drive
        :parameters
           (?user
             ?from-poi
             ?to-poi)
        :precondition
            (and
                (user-at ?user ?from-poi)
            )
        :effect
            (and
                ( user-at ?user ?to-poi)
                ( not (user-at ?user ?from-poi))
                ( increase (current-time) (drive-time ?from-poi ?to-poi) )
            )
    )
)
