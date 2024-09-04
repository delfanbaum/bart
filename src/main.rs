use bart::{
    cli::{Cli, Commands},
    project::BartProject,
};
use clap::Parser;

fn main() {
    let args = Cli::parse();
    match args.command {
        Commands::Init { directory } => {
            BartProject::init(directory);
        }
        _ => {
            println!("{:?}", args)
        }
    }
}
