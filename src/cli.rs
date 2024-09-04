use clap::{Parser, Subcommand};

use crate::build::BuildTargets;
//use chrono::{NaiveDate, Local};

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
    Init { directory: Option<String> },

    /// Adds a file to the end of the project, creating it if necessary
    Add { file: String },

    /// Removes a file to the end of the project, optionally deleting it
    Remove {
        file: String,
        #[arg(short, long)]
        delete: bool,
    },

    // Output
    /// Builds to a given target format (defaults to HTML)
    Build {
        #[arg(short, long, default_value_t=BuildTargets::Html)]
        format: BuildTargets,

        #[arg(short, long)]
        /// Optionally, build a single file
        file: Option<String>,
    },
}
