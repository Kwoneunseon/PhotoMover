
import argparse
from reader import Reader
from move import Move

def main():
  parser =  parser = argparse.ArgumentParser(description='이 프로그램은 인자를 받아서 처리합니다.')

  # 인자를 추가합니다.
  parser.add_argument('origin_folder', type=str, help='이동할 원본 폴더')
  parser.add_argument('destination_folder', type=str, help='파일을 이동할 목적지 폴더')
  parser.add_argument('--count', type=int, default=1000, help='파일 개수를 설정하고 싶을 때 사용합니다. 기본값은 1000입니다.')

  args = parser.parse_args()

  r = Reader(args.origin_folder, args.count)
  m = Move(args.destination_folder, r.process_images())
  m.process()


# 사용 예제
if __name__ == "__main__":  
  main()