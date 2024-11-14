import sys, random, socket, select, struct

class Server:
    interval_start = -1
    interval_end = -1
    thought_number = -1
    number_guessed = False
    clients_count = -1

    packer = struct.Struct('ci')
    server_addr = 0 

    # Constructor: sets up the interval, thinks a number and sets up the server
    def __init__(self, interval_start, interval_end, host, port):
        try:
            self.server_addr = (host, int(port))
            self.__initialize_interval__(interval_start, interval_end)
            self.__think_a_number__()
            self.__Setup_Server__()
        except Exception:
            print("Something went wrong... :(")
            exit(-1)

    def __Setup_Server__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(self.server_addr)
            server.listen(4)
            print("Listening for new connections...")

            inputs = [server]
            timeout = 10

            try:
                while True:
                    readable, writeable, exceptional = select.select(inputs, inputs, inputs, timeout)

                    if (self.clients_count == 0):
                        print("Every client's left. I'm leaving too...")
                        exit(0)

                    if not (readable or writeable or exceptional):
                        print("Data is not Readable/Writeable or the waiting time reached the time out...")
                        exit(-1)
                    
                    for sock in readable:
                        if sock is server: # new connection
                            client, client_addr = sock.accept()
                            inputs.append(client)
                            print("Connected: ", client_addr)
                            
                            # Checking the number of the clients
                            self.clients_count = 1 if (self.clients_count == -1) else self.clients_count + 1

                        else: # an existing connection is readable
                            data = sock.recv(self.packer.size)
                            if not data:
                                print("Logout: ", sock)
                                inputs.remove(sock)
                                sock.close()
                                self.clients_count -= 1
                            else:
                                # if someone has found the number, the game is over...
                                if (self.number_guessed):
                                    server_response = ('V'.encode(), self.thought_number)
                                    packer_data = self.packer.pack(*server_response)
                                    sock.send(packer_data)
                                    pass

                                # Receiving and sending back message to the client
                                client_response = self.packer.unpack(data)
                                print(f"\nI received this from a client: {client_response}")
                                server_response = self.__check_client_guess__(client_response)
                                print(f"I'm sending this to the client: {server_response}\n\n")
                                packer_data = self.packer.pack(*server_response)
                                sock.send(packer_data)

            except KeyboardInterrupt:
                print("Closing the server...")


    # Initializes the interval which contains the thought number
    def __initialize_interval__(self, interval_start, interval_end):
        self.interval_start = interval_start
        self.interval_end = interval_end
    
    # Generates a random number in the CLOSED interval of [self.interval_start, self.interval_end]
    def __think_a_number__(self):
        self.thought_number = random.randint(self.interval_start, self.interval_end)

    # Checks the client's guess and responses if it is correct or not
    def __check_client_guess__(self, guess):

        print(f"My thought number is: {self.thought_number}")
        if guess[0] == b"=" : # case when a client guesses a number
            if guess[1] == self.thought_number:
                self.number_guessed = True
                return ('Y'.encode(), guess[1])
            
            else:
                return ('K'.encode(), guess[1])

        else: # case when a client asks a question to be decided
            if guess[0] == b">": # client asks if the thought number is more than the guess
                return ('I'.encode(), guess[1]) if guess[1] < self.thought_number else ('N'.encode(), guess[1])
            else: # client asks if the thought number is less than the guess
                return ('I'.encode(), guess[1]) if guess[1] > self.thought_number else ('N'.encode(), guess[1])


if len(sys.argv) != 3:
    print("Not enough/too much argument")
    exit(-1)
else:
    s = Server(1,100, sys.argv[1], sys.argv[2])