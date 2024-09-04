use bart::{
    cli::{Cli, Commands},
    document::Document,
    project::BartProject,
};
use clap::Parser;

fn main() {
    let args = Cli::parse();
    match args.command {
        Commands::Init { directory } => {
            BartProject::init(directory);
        }
        Commands::Add { file } => {
            let mut project = BartProject::read_in_project();
            let doc = Document {
                path: [file].iter().collect(),
            };
            project.add_document(doc)
        }
        _ => {
            println!("{:?}", args)
        }
    }
}
