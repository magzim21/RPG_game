

# Класс Game это класс, который дергает другие классы за ниточки и заставляет работать вместе.
# Он олицетворяет принцип Композиции.
class Game:

    # Функции для хэндлеров.

    # В будущем лучше название self заменить на handler_obj
    # Или еще лучше каким-то образом использовать не handler_obj, а работать напрямую с обьектом текущей игры.
    # Возможно ли использовать встроенный self в функции находящейся в конструкторе?
    # Функция принимает алиас и пользовательский ввод и сама решает с чем ей удобнее работать. Это делает алиасы не такими привязанными к реализации функций.
    def show_inventory(gameSelf,self, alias, inp):
        player_inventory = self.get_cur_game().player.inventory
        player_name = self.get_cur_game().player.player_name
        print('Here is what {} has in inventory:'.format(player_name))
        if player_inventory:
            for thing in player_inventory:
                print(thing.oname)
        else:
            print('[Nothing]')

    def take_thing(gameSelf,self, alias, inp):
        current_room_floor = self.get_cur_game().player.get_currentroom().floor
        if not current_room_floor:
            print('Nothing to take.')
        elif len(inp.split()) > 1:
            # Можно этот код написать как-то изящнее?
            choice = ' '.join(inp.split()[1:])
            thing_selected = None
            iter_counter = 0
            for thing in current_room_floor:
                if thing.name == choice:
                    thing_selected = thing
                    thing_selected_i = iter_counter
                    break
                iter_counter += 1
            if thing_selected is not None:

                thing_popped = current_room_floor.pop(thing_selected_i)
                self.get_cur_game().player.add_thing(thing_popped)
                print('You took {}.'.format(thing_popped.name))
            else:
                print('There are no such thing as {}'.format(choice))
        else:
            print('What to take?')

    def throw_thing(gameSelf,self, alias, inp):
        player_inventory = self.get_cur_game().player.inventory
        if len(inp.split()) == 1:
            print('What to throw?')
        elif player_inventory:
            choice = ' '.join(inp.split()[1:])
            index_count = 0
            # Вижу как укоротить код
            thing_selected = None
            for thing in player_inventory:
                if thing.name == choice:
                    thing_selected = player_inventory.pop(index_count)
                index_count += 1
            if thing_selected is not None:
                self.get_cur_game().player.get_currentroom().add_thing(thing_selected)
                print('You threw {}'.format(choice))
            else:
                print('You do not have this thing.')

        else:
            print('Inventory is empty. Nothing to throw.')


    def putThing(gameSelf, ):
        pass

    def look(gameSelf,self, alias, inp):
        alias = alias.split()
        inp = inp.split()
        if len(inp) > 1:
            # Значит нужно описать предмет
            selected_thing = ' '.join(inp[1:])
            current_room_floor = self.get_cur_game().player.get_currentroom().floor
            player_inventory = self.get_cur_game().player.inventory
            for thing in current_room_floor:
                if selected_thing == thing.name:
                    print('This thing is on the floor.')
                    print(thing.full_description)
                    if thing.type == 'container' and thing.content:
                        print('This contains:')
                        for thing in thing.content:
                            print(thing.name)
            for thing in player_inventory:
                if selected_thing == thing.name:
                    print('This thing is in the inventory.')
                    print(thing.full_description)
                    if thing.type == 'container' and thing.content:
                        print('This contains:')
                        for thing in thing.content:
                            print(thing.name)

        elif len(alias) == 2:
            # Значит нужно описать сторону света
            try:
                selected_direction = alias[0]
                selected_room_name = self.get_cur_game().player.get_currentroom().get_exits()[
                    alias[0]].get_name()
                selected_room_description = self.get_cur_game().player.get_currentroom().get_exits()[
                    alias[0]].get_description()
                print(
                    '{} is located on the {} side. \nLocation description: {}\nCan\'t see what\'s on the floor.'.format(
                        selected_room_name, selected_direction, selected_room_description))
            except KeyError:
                print('There are no exits on that side.')
        elif len(inp) == 1:
            # Значит нужно описать комнату
            current_room_name = self.get_cur_game().player.get_currentroom().get_name()
            current_room_description = self.get_cur_game().player.get_currentroom().get_description()
            current_room_floor = self.get_cur_game().player.get_currentroom().floor
            print('Room name: {} \nDescription: {} '
                  .format(current_room_name, current_room_description))
            if current_room_floor:
                print('Things on the floor:')
                for thing in current_room_floor:
                    print(thing.short_description)

    def move(gameSelf,self, alias, inp):
        direction = alias.split()[0]
        exits_current_room = self.get_cur_game().player.get_currentroom().get_exits()
        if direction in exits_current_room:
            self.get_cur_game().player.set_currentroom(exits_current_room[direction])
            print('Top, top...')
            return True
        print('Auch')
        return False

    def get_commands(gameSelf,self, alias, inp):
        print('Existing commands:')
        print(', '.join(self.get_handler_aliases()))

    def __init__(self, rooms_dict, player_name, things):

        # rooms_dict {id :[название комнаты,описание, {сторона света :id комнаты]}
        # player_name  просто имя игрока
        # things предметы {room_id/inventory:(name, oname, short_description, full_description)}



        # handlers_dict {"alias": func}
        # Имеет значение в каком порядке зарегестрированы хэндллеры.
        # Если ввод из одного слова - сработает первый найденный похожий хэндлер.
        # Если ввод из нескольких слов - сработает первый найденный хэндлер похожий на ввод или хэндлер алиас которого содержится в вводе.
        # Если команда содержит алиас и дополнительные слова - последние используются или игнорируются.
        handlers_dict = {'north move': self.move, 'south move': self.move, 'east move': self.move, 'west move': self.move, 'up move': self.move,
                         'down move': self.move}
        handlers_dict.update(
            { 'north look': self.look, 'south look': self.look, 'east look': self.look, 'west look': self.look,
             'up look': self.look, 'down look': self.look,'look': self.look, }
        )
        handlers_dict.update(
            {'commands': self.get_commands, 'inventory': self.show_inventory, 'take': self.take_thing, 'throw': self.throw_thing})
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

        # Раскидывание вещей по заданным локациям
        for place, value in things.items():
            # print(value)
            if place == 'inventory':
                for thing_args in value:
                    # print(thing_args)
                    thing_creation = Thing(thing_args[0],thing_args[1],thing_args[2],thing_args[3],thing_args[4])
                    self.player.add_thing(thing_creation)
            elif place in self.rooms_dict_saved:
                for thing_args in value:
                    thing_creation = Thing(thing_args[0], thing_args[1], thing_args[2], thing_args[3],thing_args[3])
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

    def get_aliases_from_command(self, inp):
        for key, value in self.commands.items():
            if len(inp.split()) == 1:
                fist_input_word = inp.split()[0]
                if fist_input_word in key[:len(fist_input_word)]:
                    return value, key
            else:
                # Проверочный код если непонятно какая команда срабатывает
                # print(key)
                if inp in key or key in inp:
                    return value, key

    def get_handler(self, alias):
        return self.commands[alias]

    def run(self, inp):
        if self.get_aliases_from_command(inp) is None:
            return False , 'Alias not found'
        else:
            handler, alias = self.get_aliases_from_command(inp)
            handler(self, alias, inp)



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
#  совсместить сеттер и add_thing

class Thing:
    def __init__(self, name, oname, short_description, full_description, type):
        self._name = name
        self._oname = oname
        self._short_description =short_description
        self._full_description = full_description
        self._type = type
        self._content = []

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

    @property
    def type(self):
        return self._type

    @property
    def content(self):
        if self._type == 'container':
            return self._content

    @content.setter
    def content(self, thing):
        if self._type == 'container':
            self._content.append(thing)

    def content_extract(self,thing):
        counter = 0
        for item in self._content:
            if item.name == thing.name:
                break
            counter += 1
        extracted = self._content.pop(counter)
        return extracted











#Задает необходимые параметры игре


rooms_dict = {1: ['Hall', 'This is first location', {'north': 2, 'east': 3}],
              2: ['Kitchen', 'People eat here', {}],
              3: ['Bedroom''', 'People sleep here', {}]}
player_name = 'Vasya'
#{room_id/inventory:((name, oname, short_description, full_description,type),)}
things = {'inventory':(('chewing gum','chewing gum','Some box', 'Orbit, juicy water melon.', 'undefined'),),2:(('ketchup','ketchup','Glass bottle','Torchin. 100% natural tomatos','undefined'),),
          3 :(('map piece','map piece','This is top left part','The legend says...','splinter'),('pitate box','pirate box','You can pu smth here','Very big, you can put anything','container'))}
# На данный момент игрок не может знать название предмета, который хочет взять тк видит только short_description



# Инициализирует игру
first_game = Game(rooms_dict, player_name,things)

#запускает игру
first_game.play()


