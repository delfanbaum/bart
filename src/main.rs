use bart::{
    build::Builder,
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
                ..Default::default()
            };
            project.add_document(doc)
        }
        Commands::Build { format, file } => {
            let project = match file {
                Some(file) => BartProject {
                    name: file.clone(),
                    documents: vec![Document {
                        path: [file].iter().collect(),
                        ..Default::default()
                    }],
                    ..Default::default()
                },
                None => BartProject::read_in_project(),
            };
            let builder = Builder {
                project,
                target: format,
            };
            builder.build()
        }
        _ => {
            println!("{:?}", args)
        }
    }
}
