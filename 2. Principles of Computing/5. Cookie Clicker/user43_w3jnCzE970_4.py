"""
Author: Floyd Kots ~ github.com/floydkots
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
# SIM_TIME = 100000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        # self._history contains tuples each having 4 values
        # (time, item, cost_of_item, total_cookies)
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        tot_cookies = "Total cookies: %s" % self._total_cookies
        cur_cookies = "Current cookies: %s" % self._current_cookies
        cur_time = "Current time: %s" % self._current_time
        cur_cps = "Current cps: %s" % self._current_cps
        state = [tot_cookies, cur_cookies, cur_time, cur_cps]
        return "\n".join(state)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_total_cookies(self):
        """
        Return total number of cookies
        
        Should return a float too.
        """
        return self._total_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time = math.ceil((cookies - self._current_cookies) / self._current_cps)
        return time if time > 0.0 else 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            cookies = time * self._current_cps
            self._current_time += time
            self._current_cookies += cookies
            self._total_cookies += cookies
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name,
                                  cost, self._total_cookies))
#            print "Bought a %s for %.1f and got %.1f cps" % \
#                  (item_name, cost, additional_cps)
    
    def print_history(self):
        """
        Nicely print the history list
        """
        print
        print "Time".rjust(10), "Item".ljust(8), "Cost".rjust(10), "Total Cookies".rjust(10)
        for part in self._history:
            print "% 10.2f %s % 10.2f % 13.2f" % (part[0], 
                                               str(part[1]).ljust(8), 
                                               part[2], part[3])
        print
            
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    my_bi = build_info.clone()
    my_cs = ClickerState()
    
    while my_cs.get_time() <= duration:
        if my_cs.get_time() > duration:
            break
            
        item = strategy(my_cs.get_cookies(), my_cs.get_cps(), my_cs.get_history(),
                        duration - my_cs.get_time(), my_bi)
        
        if item is None:
            break

        time_until = my_cs.time_until(my_bi.get_cost(item))
        
        if my_cs.get_time() + time_until > duration:
            break
        
        my_cs.wait(time_until)
        item_cps = my_bi.get_cps(item)
        while my_cs.get_cookies() >= my_bi.get_cost(item):
            my_cs.buy_item(item, my_bi.get_cost(item), item_cps) 
            my_bi.update_item(item)
    
    if my_cs.get_time() < duration:
        my_cs.wait(duration - my_cs.get_time())
    
    return my_cs


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def build_items_cpi(build_info):
    """
    Return the list of build items as a list of tuples, 
    each tuple be like (cost_per_item, item_name)
    """
    items = []
    for item in build_info.build_items():
        items.append((build_info.get_cost(item), item))
    return items

def build_items_cpcps(build_info):
    """
    Return the list of build items as a list of tuples,
    each tuple be like (cost_per_cookie_per_second, item_name).
    """
    items = []
    for item in build_info.build_items():
        cpcps = build_info.get_cost(item) / build_info.get_cps(item)
        items.append((cpcps, item))
    return items

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    max_cookies = cookies + cps * time_left
    for item in sorted(build_items_cpi(build_info)):
        if max_cookies >= item[0]:
            return item[1]
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    max_cookies = cookies + cps * time_left
    for item in sorted(build_items_cpi(build_info), reverse=True):
        if max_cookies >= item[0]:
            return item[1]
    return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return min(build_items_cpcps(build_info))[1]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

    
def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()


    

