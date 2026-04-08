<?php
namespace DMS\LOL\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;

class LolCodeCommand extends Command
{
    protected function configure()
    {
        $this
            ->setName('lolcode:run')
            ->setDescription('Run a lolcode file')
            ->addArgument(
                'file',
                InputArgument::REQUIRED,
                'path to file'
            )
            ->addOption(
                'debug',
                'd',
                InputOption::VALUE_NONE,
                'Shows debug output if requested'
            )
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $output->writeln("<info>LOLCode Parser</info> written by <comment>Rafael Dohms</comment>, based on previous work by Tetraboy and MailChimp");
        $output->writeln("");

        $file = $input->getArgument('file');

        if (!file_exists($file)){
            $output->writeln(sprintf("<error>Unable to find the file %s</error>", $file));
            return;
        }

        $lolcode = file_get_contents($file);

        if (!is_string($lolcode)) {
            $output->writeln(sprintf("<error>Unable to read contents of file %s</error>", $file));
            return;
        }

        if ($input->getOption('debug')) {
            global $DBG;
            $DBG = true;

            $output->writeln("## Parser debug:");
        }

        $phpcode = \lol_core_parse($lolcode);

        if ($input->getOption('debug')) {

            global $DBG;
            $DBG = true;

            $output->writeln("## Generated PHP code to be executed:");
            $output->writeln(sprintf("<info>%s</info>", $phpcode));
            $output->writeln("");
        }

        eval('?>'.$phpcode.'');
    }
}
