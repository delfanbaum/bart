use super::args::{Cli, Commands};
use crate::{build::Builder, document::Document, project::BartProject};
use clap::Parser;
use std::fs;

pub fn parse() {
    let args = Cli::parse();
    match args.command {
        Commands::Init {
            name,
            byline,
            directory,
        } => BartProject::init(name, byline, directory),
        Commands::Add {
            file,
            position,
            description,
        } => {
            let mut project = BartProject::read_in_project();
            let doc = Document {
                path: [file].iter().collect(),
                description: description.unwrap_or("".to_string()),
                ..Default::default()
            };
            project.add_document(doc, position)
        }
        Commands::Build { format, file } => {
            let project = match file {
                Some(file) => BartProject::from_file(file),
                None => BartProject::read_in_project(),
            };
            let builder = Builder {
                project,
                target: format,
            };
            builder.build()
        }
        Commands::Ls => {
            let project = BartProject::read_in_project();
            println!("{}", project.print_list())
        }
        Commands::Move {
            document_position,
            new_position,
        } => {
            let mut project = BartProject::read_in_project();
            project.move_document(document_position, new_position)
        }
        Commands::Remove { file, delete } => {
            let mut project = BartProject::read_in_project();
            project.documents.retain(|doc| doc.file_name() != file);
            if delete {
                fs::remove_file(file).expect("Unable to delete file");
            }
        }
        Commands::Counts { file: _ } => todo!(),
    }
}
