use clap::{Parser, Subcommand};

use crate::build::BuildTargets;

#[derive(Debug, Parser)]
#[command(name = "bart")]
#[command(about="A project management tool for plain-text writing workflows", long_about = None)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Debug, Subcommand)]
pub enum Commands {
    // Project-level
    /// Initializes a new bart project
    Init {
        #[arg(short, long)]
        name: Option<String>,
        #[arg(short, long)]
        byline: Option<String>,
        #[arg(short, long)]
        directory: Option<String>,
    },

    /// Lists the documents (in order) included in the project
    Ls,

    /// Adds a file to the end of the project, creating it if necessary, optionally inserting it at
    /// a given position in the document list. Optionally add a description.
    Add {
        file: String,
        #[arg(short, long)]
        position: Option<usize>,
        description: Option<String>,
    },

    /// Removes a file from the project list, optionally deleting it
    Remove {
        file: String,
        #[arg(short, long)]
        delete: bool,
    },

    /// Moves a document (by position) to some other in the project (zero-indexed). To see
    /// the current document positions, run `bart ls`
    Move {
        document_position: usize,
        new_position: usize,
    },

    // Output
    /// Builds to a given target format (defaults to HTML)
    Build {
        #[arg(short, long, default_value_t=BuildTargets::Html)]
        format: BuildTargets,

        #[arg(long)]
        /// Optionally, build a single file
        file: Option<String>,
    },

    // will do word counting
    /// Refresh word counts for the project and print them, or optionally do this for a single file
    Counts { file: Option<String> },
}
