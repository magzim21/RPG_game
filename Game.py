

# Класс Game это класс, который дергает другие классы за ниточки и заставляет работать вместе.
# Он олицетворяет принцип Композиции.
class Game:
    def __init__(self, handlers_dict, rooms_dict, player_name, things):
        # handlers_dict {"alias": func}
        # rooms_dict {id :[название комнаты,описание, {сторона света :id комнаты]}
        # player_name  просто имя игрока
        # things предметы {room_id/inventory:(name, oname, short_description, full_description)}


        self.handler = Handlers()
        self.handler.set_cur_game(self)
        for alias, func in handlers_dict.items():
            self.handler.register_handler(alias, func)


        # Создание обьектов комнат
        self.rooms_dict_saved = {}
        for id, value in rooms_dict.items():
            self.rooms_dict_saved[id] = Room(value[0], value[1])

        # Связывание комнат между собой
        for id, value in rooms_dict.items():
            self.rooms_dict_saved[id].set_exits({key: value for key, value in zip(value[2].keys(),
                                                                                  [self.rooms_dict_saved[x] for x in
                                                                                   value[2].values()])})

        # Игрок будет стартовать в комнате с id==1
        room_to_start = self.rooms_dict_saved[1]
        self.player = Player(player_name, room_to_start)

        for place, thing_args in things.items():
            if place == 'inventory':
                thing_creation = Thing(thing_args[0],thing_args[1],thing_args[2],thing_args[3])
                self.player.add_thing(thing_creation)
            if place in self.rooms_dict_saved:
                thing_creation = Thing(thing_args[0], thing_args[1], thing_args[2], thing_args[3])
                self.rooms_dict_saved[place].add_thing(thing_creation)

    # Вместо main
    def play(self):
        while True:
            command = input('Введите команду:\n')
            self.handler.run(command)


class Handlers:
    def __init__(self):
        self.commands = {}
        self.__cur_game = None

    def set_cur_game(self, game):
        self.__cur_game = game

    def get_cur_game(self):
        return self.__cur_game

    def register_handler(self, alias, func):
        self.commands[alias] = func

    def unregister_handler(self, alias):
        if self.commands.pop(alias, None) is None:
            return False, "Alias was not found"
        else:
            return True, "Command deleted successfully"

    def get_handler_aliases(self):
        return self.commands.keys()

    def get_aliases_from_command(self, inp1):
        for key, value in self.commands.items():
            if inp1 in key[:len(inp1)]:
                return value, key


    def get_handler(self, alias):
        return self.commands[alias]

    def run(self, inp):
        if self.get_aliases_from_command(inp) is None:
            return False , 'Alias not found'
        else:
            handler, full_alias = self.get_aliases_from_command(inp)
            handler(self, full_alias)



class Room:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
        self.exits = {}
        self._floor = []

    def set_exits(self, exits):
        opp_dir_dict = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east', 'up': 'down', 'down': 'up'}
        for direction, room in exits.items():

            if direction not in self.get_exits():
                self.exits[direction] = room

            if opp_dir_dict[direction] not in room.get_exits():
                room.set_exits({opp_dir_dict[direction]: self})

    # Добавить проверки и автодобавление выходов в добавляемую комнату.

    def get_exits(self):
        return self.exits

    def get_name(self):
        return self.__name

    def get_description(self):
        #Проще дописать этот метод, чем переписывать все вызовы описания
        return self.__description

    @property
    def floor(self):
        return self._floor

    @floor.setter
    def floor(self, things):
        self._floor = things

    def add_thing(self, thing):
        self._floor.append(thing)





class Player:
    def __init__(self, player_name, currentroom=None):
        self._player_name = player_name
        self.currentroom = currentroom
        self._inventory = []

    def get_currentroom(self):
        return self.currentroom

    def set_currentroom(self, value):
        self.currentroom = value

    @property
    def player_name(self):
        return self._player_name

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, things):
        self._inventory = things

    def add_thing(self,thing):
        self._inventory.append(thing)


class Thing:
    def __init__(self, name, oname, short_description, full_description):
        self._name = name
        self._oname = oname
        self._short_description =short_description
        self._full_description = full_description

    @property
    def name(self):
        return self._name

    @property
    def oname(self):
        return self._oname

    @property
    def short_description(self):
        return self._short_description

    @property
    def full_description(self):
        return self._full_description




# Функции для хэндлеров.
def show_inventory(self, alias):
    player_inventory = self.get_cur_game().player.inventory
    player_name = self.get_cur_game().player.player_name
    print('Here is what {} has in inventory:'.format(player_name))
    if player_inventory:
        for thing in player_inventory:
            print(thing.oname)
    else:
        print('[Nothing]')

def take_thing(self, alias):
    current_room_floor = self.get_cur_game().player.get_currentroom().floor
    if not current_room_floor:
        print('Nothing to take.')
    elif len(current_room_floor):
        thing_popped = current_room_floor.pop()
        self.get_cur_game().player.add_thing(thing_popped)
        print('You took {}.'.format(thing_popped.name))
    else:
        choice = input('What thing to take?\n')
        thing_choosed = None
        for thing in current_room_floor:
            if thing.name == choice:
                thing_choosed = thing
        if thing_choosed is not None:
            thing_popped = current_room_floor.pop(thing_choosed)
            self.get_cur_game().player.add_thing(thing_popped)
            print('You took {}.'.format(thing_popped))
        else:
            print('There are no such thing as {}'.format(choice))

def throw_thing(self,alias):
    player_inventory = self.get_cur_game().player.inventory
    if player_inventory:
        choice = input('What thing to throw?\n')
        index_count = 0
        thing_choosed = None
        for thing in player_inventory:
            if thing.name == choice:
                thing_choosed = player_inventory.pop(index_count)
            index_count +=1
        if thing_choosed is not None:
            self.get_cur_game().player.get_currentroom().add_thing(thing_choosed)
            print('You threw {}'.format(choice))
        else:
            print('You do not have this thing.')

    else:
        print('Inventory is empty. Nothing to throw.')




def look(self, alias):
    direction = alias.split()
    if len(direction) == 2:
        try:
            selected_direction = direction[0]
            selected_room_name = self.get_cur_game().player.get_currentroom().get_exits()[direction[0]].get_name()
            selected_room_description = self.get_cur_game().player.get_currentroom().get_exits()[direction[0]].get_description()
            print('{} is located on the {} side. \nLocation description: {}\nCan\'t see what\'s on the floor.'.format(selected_room_name, selected_direction,selected_room_description))
        except KeyError:
            print('There are no exits on that side.')
    else:
        current_room_name = self.get_cur_game().player.get_currentroom().get_name()
        current_room_description = self.get_cur_game().player.get_currentroom().get_description()
        current_room_floor = self.get_cur_game().player.get_currentroom().floor
        print('Room name: {} \nDescription: {} '
              .format(current_room_name,current_room_description))
        if current_room_floor:
            print('Things on the floor:')
            for thing in current_room_floor:
                print(thing.short_description)


def move(self, alias):
    direction = alias.split()[0]
    exits_current_room = self.get_cur_game().player.get_currentroom().get_exits()
    if direction in exits_current_room:
        self.get_cur_game().player.set_currentroom(exits_current_room[direction])
        print('Top, top...')
        return True
    print('Auch')
    return False

def get_commands(self, alias):
    print('Existing commands:')
    print(', '.join(self.get_handler_aliases()))





#Задает необходимые параметры игре

handlers_dict = {'north move': move, 'south move': move, 'east move': move, 'west move': move, 'up move': move, 'down move': move}
handlers_dict.update(
    {'look': look, 'north look': look, 'south look': look, 'east look': look, 'west look': look, 'up look': look, 'down look': look,}
)
handlers_dict.update({'commands':get_commands,'inventory': show_inventory, 'take':take_thing,'throw':throw_thing})
rooms_dict = {1: ['Hall', 'This is first location', {'north': 2, 'east': 3}],
              2: ['Kitchen', 'People eat here', {}],
              3: ['Bedroom''', 'People sleep here', {}]}
player_name = 'Vasya'
#{room_id/inventory:(name, oname, short_description, full_description)}
things = {'inventory':('chewing gum','chewing gum','Looks like it is new.', 'Orbit, juicy water melon.'),2:('ketchup','ketchup','Glass bottle','Torchin. 100% natural tomatos')}



# Инициализирует игру
first_game = Game(handlers_dict, rooms_dict, player_name,things)


#запускает игру
first_game.play()

