from argparse import ArgumentParser
import os
import logging
import random
import shutil

from toil.job import Job


def setup(job, input_file, n, down_checkpoints):
    """Sets up the sort.
    """
    # Write the input file to the file store
    input_filestore_id = job.fileStore.writeGlobalFile(input_file, True)
    job.fileStore.logToMaster(" Starting the merge sort ")
    job.addFollowOnJobFn(cleanup, job.addChildJobFn(down,
                                                    input_filestore_id, n,
                                                    down_checkpoints=down_checkpoints,
                                                    memory='1000M').rv(), input_file)


def make_file_to_sort(file_name, lines, line_length):
    with open(file_name, 'w') as fileHandle:
        for _ in xrange(lines):
            line = "".join(random.choice('actgACTGNXYZ') for _ in xrange(line_length - 1)) + '\n'
            fileHandle.write(line)


def main():
    parser = ArgumentParser()
    Job.Runner.addToilOptions(parser)

    parser.add_argument('--num-lines', default=1000, help='Number of lines in file to sort.', type=int)
    options = parser.parse_args()

    make_file_to_sort(file_name='file_to_sort.txt', lines=options.num_lines, line_length=options.line_length)

    # Now we are ready to run
    Job.Runner.startToil(Job.wrapJobFn(setup, os.path.abspath('file_to_sort.txt'), int(options.N), False,
                                       memory='1000M'), options)

if __name__ == '__main__':
    main()