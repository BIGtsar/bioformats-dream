import os
import argparse
from sam import SamReader


def main():
    parser = argparse.ArgumentParser(description='Анализатор SAM файлов')
    parser.add_argument('-f', '--file', required=True, help='Путь к SAM файлу')
    parser.add_argument('-s', '--stats', action='store_true', help='Только статистика')
    parser.add_argument('-a', '--alignments', type=int, default=3, help='Число выравниваний для показа')
    parser.add_argument('-c', '--chromosome', help='Фильтр по хромосоме')
    
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Ошибка: файл {args.file} не найден")
        return

    analyze_sam(args)


def analyze_sam(args):
    print(f"Анализ файла: {args.file}")
    print("=" * 50)
    
    with SamReader(args.file) as reader:
        # Базовая статистика
        header = reader.get_header()
        total = reader.count_alignments()
        chroms = reader.get_chromosomes()
        
        print(f"Выравниваний: {total}")
        print(f"Хромосомы: {', '.join(chroms[:5])}")
        print(f"Строк в заголовке: {len(header)}")
        print()

        if not args.stats:
            # Показ выравниваний
            print(f"Первые {args.alignments} выравниваний:")
            print("-" * 30)
            
            count = 0
            for alignment in reader.read():
                if count >= args.alignments:
                    break
                    
                if args.chromosome and alignment.chrom != args.chromosome:
                    continue
                
                print(f"{count+1}. {alignment.qname}")
                print(f"   Хромосома: {alignment.chrom}, Позиция: {alignment.pos}")
                print(f"   Качество: {alignment.mapq}, Флаг: {alignment.flag}")
                print(f"   CIGAR: {alignment.cigar}")
                print()
                count += 1


if __name__ == "__main__":
    main()
