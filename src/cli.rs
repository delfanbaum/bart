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

    /// Adds a file to the end of the project, creating it if necessary
    Add {
        file: String,
        #[arg(short, long)]
        position: Option<u8>,
    },

    /// Removes a file (by name or position) to the end of the project, optionally deleting it
    Remove {
        #[arg(short, long)]
        file: Option<String>,
        #[arg(short, long)]
        delete: bool,
    },

    // TODO figure out an indexing scheme that makes sense; maybe moves to position, moving
    // everything else down
    /// Moves a document to the provided position in the project
    Move {
        file: String,
        #[arg(short, long)]
        position: u8,
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
    Counts
}
