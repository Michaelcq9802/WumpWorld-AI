from Agent import Agent
import queue
class MyAI ( Agent ):

    def __init__ ( self ):
        self.startrm = (1,1)
        self.current = (1,1)
        self.last_rm = (1,1)
        self.facing = 'r'
        self.safe_rm = []
        self.pit_location = dict()
        self.wumpus_location = dict()
        self.rm_history = []
        self.step_to_take = []
        self.made_turn = False
        self.got_gold = False
        self.escape = False 
        self.size = [50,50]
        self.wumpus_dead = False
        self.arrow = True
        self.wumpus_found = False

    def getAction( self, stench, breeze, glitter, bump, scream ):
        if self.current not in self.rm_history:    
            self.rm_history.append(self.current)

        if self.current in self.safe_rm:
            self.safe_rm.remove(self.current)
        if self.current in self.pit_location:
            del self.pit_location[self.current]
        if self.current in self.wumpus_location:
            del self.wumpus_location[self.current]

        if len(self.step_to_take) != 0:
            move = self.step_to_take[-1]
            del self.step_to_take[-1]
            return move


        if self.current == self.startrm and (self.got_gold or self.escape):
            return Agent.Action.CLIMB
        elif (self.got_gold or self.escape) and self.current != self.startrm:
            return self.move(self.facing, self.same_way_out())

        if glitter:
            self.got_gold = True
            return Agent.Action.GRAB 

        if self.current == self.startrm and breeze:
            return Agent.Action.CLIMB

        if scream:
            self.wumpus_dead = True

        if self.current == self.startrm:
            if stench and not self.wumpus_dead:
                if self.arrow == True:
                    self.arrow = False
                    return Agent.Action.SHOOT
                elif self.arrow == False:
                    self.wumpus_found = True
                    self.wumpus_location[(1,2)] = True

        if bump:
            if self.facing == "r":
                self.size[0] = self.current[0]
                self.current = self.last_rm
                x = []
                for rm in self.safe_rm:
                    if rm[0] >= self.size[0]:
                        x.append(rm)
                for rm in x:
                    self.safe_rm.remove(rm)
                    if rm in self.wumpus_location:
                        del self.wumpus_location[rm]
                    if rm in self.pit_location:
                        del self.pit_location[rm]
                return self.next_move()
            elif self.facing == "u":
                self.size[1] = self.current[1]
                self.current = self.last_rm
                x = []
                for rm in self.safe_rm:
                    if rm[1] >= self.size[1]:
                        x.append(rm)
                for rm in x:
                    self.safe_rm.remove(rm)
                    if rm in self.wumpus_location:
                        del self.wumpus_location[rm]
                    if rm in self.pit_location:
                        del self.pit_location[rm]
                return self.next_move()

        if breeze and stench:
            possible_threat = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            if len(self.wumpus_location) >= 1:
                x = []
                for rm in self.wumpus_location:
                    if rm not in possible_threat or self.is_move_valid(rm) == False:
                        x.append(rm)
                for rm in x:
                    del self.wumpus_location[rm]

            if self.wumpus_dead == True:
                for rm in possible_threat:
                    if self.is_move_valid(rm)  == True and rm not in self.rm_history:
                        if rm in self.wumpus_location and rm not in self.pit_location:
                            del self.wumpus_location[rm]
                            self.safe_rm.append(rm)
                        else:
                            self.pit_location[rm] = True
                return self.next_move()

            elif len(self.wumpus_location) == 1 and self.arrow and not self.wumpus_dead:
                if self.ready(list(self.wumpus_location.keys())[0]) == True:
                    if len(self.step_to_take) != 0:
                        move = self.step_to_take[-1]
                        del self.step_to_take[-1]
                        return move
                    self.arrow = False
                    return Agent.Action.SHOOT     

            for rm in possible_threat:
                if self.is_move_valid(rm) == True and rm not in self.rm_history:
                    self.pit_location[rm] = True
                    self.wumpus_location[rm] = True
            return self.next_move()

        if breeze:
            possible_threat = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            for rm in possible_threat:
                if self.is_move_valid(rm) == True and rm not in self.rm_history:
                    if rm in self.wumpus_location and rm not in self.pit_location:
                        del self.wumpus_location[rm]
                        self.safe_rm.append(rm)
                    else:
                        self.pit_location[rm] = True
            return self.next_move()

        if stench:
            possible_threat = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            if self.wumpus_found == True:
                for rm in possible_threat:
                    if self.is_move_valid(rm) == True and rm not in self.rm_history and rm not in self.wumpus_location:
                        self.safe_rm.append(rm)
                        if rm in self.pit_location:
                            del self.pit_location[rm]
                        if rm in self.wumpus_location:
                            del self.wumpus_location[rm]
                if len(self.safe_rm) > 0:
                    return self.next_move()
                else:
                    self.escape = True
                    return self.next_move()

            if len(self.wumpus_location) >= 1:
                x = []
                for rm in self.wumpus_location:
                    if rm not in possible_threat or self.is_move_valid(rm) == False:
                         x.append(rm)
                for rm in x:
                    del self.wumpus_location[rm]
            if self.wumpus_dead == True:
                for rm in possible_threat:
                    if self.is_move_valid(rm) == True and rm not in self.rm_history:
                        self.safe_rm.append(rm)
                        if rm in self.pit_location:
                            del self.pit_location[rm]
                        if rm in self.wumpus_location:
                            del self.wumpus_location[rm]
                if len(self.safe_rm) > 0:
                    return self.next_move()
                else:
                    self.escape = True
                    return self.next_move()

            elif len(self.wumpus_location) == 1 and self.arrow and not self.wumpus_dead:
                if self.ready(list(self.wumpus_location.keys())[0]) == True:
                    if len(self.step_to_take) != 0:
                        move = self.step_to_take[-1]
                        del self.step_to_take[-1]
                        return move
                    self.arrow = False
                    return Agent.Action.SHOOT
                                 
            else:
                for rm in possible_threat:
                    if self.is_move_valid(rm)  == True and rm not in self.rm_history:
                        if rm in self.pit_location and rm not in self.wumpus_location:
                            del self.pit_location[rm]
                            self.safe_rm.append(rm)
                        else:
                            self.wumpus_location[rm] = True
            return self.next_move()
        
        else:
            safe = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]),(self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
            for rm in safe:
                if self.is_move_valid(rm) == True and rm not in self.rm_history:
                    self.safe_rm.append(rm)
                    if rm in self.pit_location:
                        del self.pit_location[rm]
                    if rm in self.wumpus_location:
                        del self.wumpus_location[rm]
            if len(self.safe_rm) > 0:
                return self.next_move()
            else:
                self.escape = True
                return self.next_move()

    def turnback(self):
        if self.made_turn == True:
            self.step_to_take.append(Agent.Action.FORWARD)
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            self.made_turn = False
        else:
            self.step_to_take.append(Agent.Action.FORWARD)
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            self.step_to_take.append(Agent.Action.TURN_LEFT)

    def is_rm_adjacent(self, rm):
        if (rm[0] == self.current[0] + 1 or self.current[0] - 1) and rm[1] == self.current[1]:
            return True
        elif (rm[1] == self.current[1] + 1 or self.current[1] - 1) and rm[0] == self.current[0]:
            return True
        else:
            return False

    def is_move_valid(self, rm):
        in_bound = True
        if rm[0] >= self.size[0] or rm[1] >= self.size[1] or rm[0] <= 0 or rm[1] <= 0:
            in_bound = False
        if in_bound == True:
            return self.is_rm_adjacent(rm)
        else:
            return False

    def move(self, facing, rm):
        if rm[0] == self.current[0] + 1:
            return self.action_to_take('r', facing, rm)
        elif rm[0] == self.current[0] - 1:
            return self.action_to_take('l', facing, rm)
        elif rm[1] == self.current[1] + 1:
            return self.action_to_take('u', facing, rm)
        elif rm[1] == self.current[1] - 1:
            return self.action_to_take('d', facing, rm)

    def action_to_take(self, direction, facing, rm):
        if direction == 'r':
            if self.facing == "r":
                self.last_rm = self.current
                self.current = rm
                return Agent.Action.FORWARD
            elif self.facing == "u":
                self.facing = "r"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_RIGHT
            elif self.facing == "d":
                self.facing = "r"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_LEFT
            elif self.facing == "l":
                self.facing = "r"
                self.last_rm = self.current
                self.current = rm
                self.made_turn = True
                self.turnback()
                return Agent.Action.TURN_LEFT
        elif direction == 'l':
            if self.facing == "l":
                self.last_rm = self.current
                self.current = rm
                return Agent.Action.FORWARD
            elif self.facing == "u":
                self.facing = "l"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_LEFT
            elif self.facing == "d":
                self.facing = "l"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_RIGHT
            elif self.facing == "r":
                self.facing = "l"
                self.last_rm = self.current
                self.current = rm
                self.made_turn = True
                self.turnback()
                return Agent.Action.TURN_LEFT
        elif direction == 'u':
            if self.facing == "u":
                self.last_rm = self.current
                self.current = rm
                return Agent.Action.FORWARD
            elif self.facing == "l":
                self.facing = "u"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_RIGHT
            elif self.facing == "r":
                self.facing = "u"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_LEFT
            elif self.facing == "d":
                self.facing = "u"
                self.last_rm = self.current
                self.current = rm
                self.made_turn = True
                self.turnback()
                return Agent.Action.TURN_LEFT
        elif direction == 'd':
            if self.facing == "d":
                self.last_rm = self.current
                self.current = rm
                return Agent.Action.FORWARD
            elif self.facing == "r":
                self.facing = "d"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_RIGHT
            elif self.facing == "l":
                self.facing = "d"
                self.last_rm = self.current
                self.current = rm
                self.step_to_take.append(Agent.Action.FORWARD)
                return Agent.Action.TURN_LEFT
            elif self.facing == "u":
                self.facing = "d"
                self.last_rm = self.current
                self.current = rm
                self.made_turn = True
                self.turnback()
                return Agent.Action.TURN_LEFT

    def same_way_out(self):
        for rm in self.rm_history:
            if self.is_rm_adjacent(rm):
                if (self.current[0] - 1 == rm[0] and self.current[1] == rm[1]) or (self.current[0] == rm[0] and self.current[1] - 1 == rm[1]):
                    self.rm_history.remove(self.current)
                    return rm

        possible_rm = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]), (self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
        for rm in possible_rm:
            if self.is_move_valid(rm) and rm != self.last_rm:
                return rm
            else:
                return self.last_rm

    def ready(self, rm):
        if self.current[0]  < rm[0] and self.current[1] == rm[1] and self.facing == 'r':
            return True
        elif self.current[0] <  rm[0] and self.current[1] == rm[1] and self.facing == 'u':
            self.facing = 'r'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[0] <  rm[0] and self.current[1] == rm[1] and self.facing == 'l':
            self.facing = 'r'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[0] <  rm[0] and self.current[1] == rm[1] and self.facing == 'd':
            self.facing = 'r'
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            return True
        elif self.current[0]  > rm[0] and self.current[1] == rm[1] and self.facing == 'l':
            return True
        elif self.current[0]  > rm[0] and self.current[1] == rm[1] and self.facing == 'd':
            self.facing = 'l'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[0]  > rm[0] and self.current[1] == rm[1] and self.facing == 'r':
            self.facing = 'l'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[0]  > rm[0] and self.current[1] == rm[1] and self.facing == 'u':
            self.facing = 'l'
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            return True
        elif self.current[1] <  rm[1] and self.current[0] == rm[0] and self.facing == 'u':
            return True
        elif self.current[1] <  rm[1] and self.current[0] == rm[0] and self.facing == 'l':
            self.facing = 'u'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[1] <  rm[1] and self.current[0] == rm[0] and self.facing == 'd':
            self.facing = 'u'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[1] < rm[1] and self.current[0] == rm[0] and self.facing == 'r':
            self.facing = 'u'
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            return True
        elif self.current[1] > rm[1] and self.current[0] == rm[0] and self.facing == 'd':
            return True
        elif self.current[1]  > rm[1] and self.current[0] == rm[0] and self.facing == 'r':
            self.facing = 'd'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[1]  > rm[1] and self.current[0] == rm[0] and self.facing == 'u':
            self.facing = 'd'
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            self.step_to_take.append(Agent.Action.TURN_RIGHT)
            return True
        elif self.current[1]  > rm[1] and self.current[0] == rm[0] and self.facing == 'l':
            self.facing = 'd'
            self.step_to_take.append(Agent.Action.TURN_LEFT)
            return True

    def next_move(self):
        possible_rm = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]), (self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
        for rm in possible_rm:
            if self.is_move_valid(rm) and rm != self.current:
                if rm in self.safe_rm:
                    return self.move(self.facing, rm)
        if len(self.safe_rm) > 0:
            sr = list(self.safe_rm)[0]
            best = None
            for rm in possible_rm:
                if self.is_move_valid(rm) and rm in self.rm_history:
                    best = rm
            for rm in possible_rm:
                if rm in self.rm_history and self.is_move_valid(rm) and rm != self.last_rm:
                    if abs(sr[0] - rm[0]) < abs(sr[0] - best[0]) or abs(sr[1] - rm[1]) < abs(sr[1] - best[1]):
                        best = rm
            return self.move(self.facing, best)
        else:
            self.escape = True
            rm = self.same_way_out()
            return self.move(self.facing, rm)
            
