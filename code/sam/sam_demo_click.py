import os
import click
from sam import SamReader


@click.command()
@click.option('-f', '--file', required=True, help='Путь к SAM файлу')
@click.option('-s', '--stats', is_flag=True, help='Показать только статистику')
@click.option('-a', '--alignments', default=3, help='Количество выравниваний для показа')
@click.option('-c', '--chromosome', help='Фильтр по хромосоме')
@click.option('--show-header', is_flag=True, help='Показать заголовок файла')
def main(file, stats, alignments, chromosome, show_header):
    """Простой анализатор SAM файлов"""
    
    if not os.path.exists(file):
        click.echo(f"Ошибка: файл {file} не найден", err=True)
        return

    analyze_sam(file, stats, alignments, chromosome, show_header)


def analyze_sam(file, stats, alignments, chromosome, show_header):
    click.echo(f"Анализ файла: {file}")
    click.echo("=" * 50)
    
    with SamReader(file) as reader:
        # Базовая статистика
        header = reader.get_header()
        total = reader.count_alignments()
        chroms = reader.get_chromosomes()
        
        click.echo(f"Выравниваний: {total}")
        click.echo(f"Хромосомы: {', '.join(chroms[:5])}")
        click.echo(f"Строк в заголовке: {len(header)}")
        
        # Показать заголовок если нужно
        if show_header:
            click.echo("\nЗаголовок файла:")
            click.echo("-" * 30)
            for i, line in enumerate(header[:5]):
                click.echo(f"{i+1}. {line[:80]}...")
        
        click.echo()

        if not stats:
            # Показ выравниваний
            click.echo(f"Первые {alignments} выравниваний:")
            click.echo("-" * 30)
            
            count = 0
            for alignment in reader.read():
                if count >= alignments:
                    break
                    
                if chromosome and alignment.chrom != chromosome:
                    continue
                
                click.echo(click.style(f"{count+1}. {alignment.qname}", fg='green'))
                click.echo(f"   Хромосома: {alignment.chrom}, Позиция: {alignment.pos}")
                click.echo(f"   Качество: {alignment.mapq}, Флаг: {alignment.flag}")
                click.echo(f"   CIGAR: {alignment.cigar}")
                click.echo()
                count += 1


if __name__ == "__main__":
    main()
