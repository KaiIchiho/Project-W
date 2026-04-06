from core.sub_phase.phase_base import Phase

class StandbyPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Standby Phase"
        self.next_phase=None
        self.handlers={
            
        }