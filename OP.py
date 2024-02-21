import psutil

'''

# Задание 1
class Process:
    def __init__(self, pr_id, pages):
        self.pr_id = pr_id
        self.pages = pages

def find_process(disk, pr_id):
    for ind, process in enumerate(disk):
        if process.pr_id == pr_id:
            return ind
    return -1

def frequency(freqes):
    min = 10000000
    res = -1
    for i, freq in enumerate(freqes):
        if freq < res:
            res = freq
            min = i
    return min

def main():
    disk = []
    with open("virtual_disk.txt", "r") as file:
        for _ in range(3):
            process, page, data = map(int, file.readline().split())
            ind = find_process(disk, process)
            if ind == -1:
                new_map = {page: data}
                disk.append(Process(process, new_map))
            else:
                disk[ind].pages[page] = data
    ram_size = 8
    ram = []
    req = [0] * ram_size
    map_ = {}
    for p in disk:
        for page in p.pages:
            map_.setdefault(p.pr_id, {})[page] = 0
    print("Enter process id, page id:")
    while True:
        try:
            process, page = map(int, input().split())
        except ValueError:
            print("Invalid input. Please enter process id and page id.")
            continue
        ind = find_process(disk, process)
        if ind == -1 or page not in disk[ind].pages:
            print("Invalid process or page id.")
            continue
        if not map_[process][page]:
            print("Page moved from virtual ram.")
            if len(ram) == ram_size:
                removed_pid = frequency(req)
                removed_pr = ram[removed_pid]
                map_[removed_pr[0]][removed_pr[1]] = 0
                ram[removed_pid] = (process, page, disk[ind].pages[page])
                map_[process][page] = removed_pid
                req[removed_pid] = 1
                print("Page data:", ram[removed_pid][2])
                print("Index in ram:", removed_pid)
                print("Removed page:", removed_pr[0], removed_pr[1])
            else:
                ram.append((process, page, disk[ind].pages[page]))
                insert_ind = len(ram) - 1
                map_[process][page] = insert_ind
                req[insert_ind] = 1
                print("Page data:", ram[insert_ind][2])
                print("Index in ram:", insert_ind)
        else:
            req_id = map_[process][page]
            req[req_id] += 1
            print("Page data:", ram[req_id][2])
            print("Index in ram:", req_id)
if __name__ == "__main__":
    main()
'''
'''
def main():
     memory = psutil.virtual_memory()
     total = memory.total
     free = memory.available
     print("Кол-во стр физ памяти:", total)
     print("Кол-во стр свободной физ памяти:", free)
if __name__ == "__main__":
 main()
'''
'''
def convert_bytes_to_gb(bytes):
     return bytes / (1024 ** 3)
def memory_info():
      phmem = psutil.virtual_memory()
      tot_phmem = convert_bytes_to_gb(phmem.total)
      diskmem = psutil.disk_usage('/')
      tot_diskmem = convert_bytes_to_gb(diskmem.total)
      per_phmem = (phmem.used / phmem.total) * 100
      return {
      "tot_phmem": tot_phmem,
      "tot_diskmem": tot_diskmem,
      "per_phmem": per_phmem
      }
if __name__ == "__main__":
      memory_info = memory_info()
      print(f"Объем оперативной памяти: {memory_info['tot_phmem']:.2f} GB")
      print(f"Объем дисковой памяти: {memory_info['tot_diskmem']:.2f} GB")
      print(f"Процент использования оперативной памяти: {memory_info['per_phmem']:.2f}%")
'''

'''

class Node:
      def __init__(self, name):
            self.name = name
class File(Node):
      def __init__(self, name, size):
            super().__init__(name)
            self.size = size
class Directory(Node):
      def __init__(self, name):
            super().__init__(name)
            self.children = []
      def get_size(self):
            total_size = 0
            for child in self.children:
                  if isinstance(child, File):
                        total_size += child.size
                  elif isinstance(child, Directory):
                        total_size += child.get_size()
            return total_size
def convert_size(size):
      if size // 1024 != 0:
            return f"{size // 1024} KB"
      else:
            return f"{size} B"
class Filesystem:
      def __init__(self, max_size, cluster_size):
            self.size = 0
            self.max_size = max_size // cluster_size
            self.cluster_size = cluster_size
            self.root = Directory("/")
            self.curr_path = [self.root]
      def path_to_string(self):
            path_str = ""
            for directory in self.curr_path:
                  path_str += directory.name
                  if directory.name != "/":
                        path_str += "/"
            return path_str
      def disk_usage(self):
            used_space = self.size * self.cluster_size
            free_space = (self.max_size - self.size) * self.cluster_size
            total_space = self.max_size * self.cluster_size
            return f"Used: {convert_size(used_space)}\nFree:{convert_size(free_space)}\nSpace: {convert_size(total_space)}"
      def make_directory(self, path):
            copy = self.curr_path[:]
            name = self.parse_path(path)[-1]
            path = path[:path.rfind(name)]
            res = self.cd(copy, path)
            if res:
                  for node in copy[-1].children:
                        if node.name == name:
                              return False
                  new_directory = Directory(name)
                  copy[-1].children.append(new_directory)
                  return True
            return False
      def make_file(self, path, size):
             copy = self.curr_path[:]
             name = self.parse_path(path)[-1]
             path = path[:path.rfind(name)]
             res = self.cd(copy, path)
             if res:
                  for node in copy[-1].children:
                        if node.name == name:
                              return False
                  file_size = size // self.cluster_size + (size % self.cluster_size > 0)
                  new_file = File(name, file_size)
                  copy[-1].children.append(new_file)
                  self.size += file_size
                  return True
             return False
      def remove(self, path):
             copy = self.curr_path[:]
             name = self.parse_path(path)[-1]
             path = path[:path.rfind(name)]
             res = self.cd(copy, path)
             if res:
                  for i, node in enumerate(copy[-1].children):
                        if node.name == name:
                              if isinstance(node, File):
                                    self.size -= node.size
                              elif isinstance(node, Directory):
                                    self.curr_path = copy
                                    copy[-1].children.pop(i)
                                    return True
             return False
      def ls(self):
            file_list = []
            for node in self.curr_path[-1].children:
                  if isinstance(node, File):
                        file_list.append([f"file: {node.name}", str(node.size * self.cluster_size)])
                  elif isinstance(node, Directory):
                        file_list.append([f"dir: {node.name}", str(node.get_size() * self.cluster_size)])
            return file_list
      def move(self, file_path, dest_path):
            return self.copy(file_path, dest_path) and self.remove(file_path)
      def copy(self, file_path, dest_path):
            copy = self.curr_path[:]
            name = self.parse_path(file_path)[-1]
            res = self.cd(copy, file_path)
            to_copy = None
            for node in copy[-1].children:
                  if node.name == name:
                         to_copy = node
                         break
            if to_copy is None:
                  return False
            copy = self.curr_path[:]
            res = self.cd(copy, dest_path)
            for node in copy[-1].children:
                  if node.name == name:
                        return False
            if isinstance(to_copy, File):
                  copy[-1].children.append(File(to_copy.name, to_copy.size))
                  self.size += to_copy.size
            elif isinstance(to_copy, Directory):
                   copy[-1].children.append(Directory(to_copy.name))
                   self.size += to_copy.get_size()
            return True
      def cd(self, curr_path, path):
             splitted = self.parse_path(path)
             ptr = 0
             if splitted[0] == "/":
                   curr_path = [curr_path[0]]
                   ptr = 1
             while ptr < len(splitted):
                  if splitted[ptr] == "." or splitted[ptr] == "":
                        pass
                  elif splitted[ptr] == "..":
                        if len(curr_path) > 1:
                              curr_path.pop()
                  else:
                        found = False
                        for node in curr_path[-1].children:
                              if isinstance(node, Directory):
                                    if node.name == splitted[ptr]:
                                          curr_path.append(node)
                                          found = True
                        if not found:
                              return False
                  ptr += 1
             return True
      @staticmethod
      def parse_path(path):
             res = path.split("/")
             if res[0] == "":
                  res[0] = "/"
             return res
if __name__ == "__main__":
       filesystem = Filesystem(65536, 512)
       filesystem.make_directory("Desktop")
       filesystem.make_directory(".config")
       filesystem.make_directory("Downloads")
       filesystem.make_directory("Documents")
       filesystem.make_directory("Pictures")
       while True:
             print(filesystem.path_to_string(), " > ", end="")
             line = input()
             args = line.split(" ")
             if args[0] == "mkdir":
                  if len(args) >= 2:
                        res = filesystem.make_directory(args[1])
                        if not res:
                              print("Unable to create directory")
                  else:
                        print("Invalid command. Usage: mkdir <directory_name>")
             elif args[0] == "cd":
                  if ":" in args[1]:
                        filesystem.curr_path = [filesystem.root]
                        drive, path = args[1].split("\\", 1)
                        if drive and path:
                              if not filesystem.cd(filesystem.curr_path, path):
                                    print(f"Directory '{path}' not found on drive '{drive}'")
                  else:
                        if filesystem.cd(filesystem.curr_path, args[1]):
                              filesystem.curr_path = filesystem.curr_path
                        else:
                              print(f"Directory '{args[1]}' not found")
             elif args[0] == "touch":
                  if len(args) == 2:
                         args.append("512")
                         filesystem.make_file(args[1], int(args[2]))
             elif args[0] == "ls":
                  files = filesystem.ls()
                  for file in files:
                        print(f"- {file[0]} {convert_size(int(file[1]))}")
             elif args[0] == "du":
                  print(filesystem.disk_usage())
             elif args[0] == "rm":
                  res = filesystem.remove(args[1])
                  if not res:
                        print("Unable to remove: ", args[1])
                  else:
                        print("Successfully removed: ", args[1])
             elif args[0] == "cp":
                   res = filesystem.copy(args[1], args[2])
                   if not res:
                        print("Unable to copy: ", args[1])
                   else:
                        print("Successfully copied to: ", args[2])
             elif args[0] == "mv":
                   res = filesystem.move(args[1], args[2])
                   if not res:
                        print("Unable to move: ", args[1])
                   else:
                        print("Successfully moved to: ", args[2])

'''

import time
def keyboard_buffer(frequency):
    buffer = ""
    print("Введите текст (для завершения введите '0'): ")
    while True:
        user_input = input()
        if user_input == "0":
            break
        buffer += user_input + "\n"
    while True:
        if len(buffer) > 0:
            print(buffer[0], end="")
            buffer = buffer[1:]
            time.sleep(1.0 / frequency)
        else:
            break
if __name__ == "__main__":
    frequency = float(input("Введите частоту передачи: "))
    keyboard_buffer(frequency)