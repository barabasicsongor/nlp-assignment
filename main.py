from io_manager import read_emails

if __name__ == '__main__':
  testing = True # Indicates whether in testing mode or not
  save = False # Indicates whether it should save the produced output or not
  path_train = './Data/training/'

  # Read training data
  emails_train = read_emails(path_train)