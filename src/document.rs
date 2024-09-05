use core::panic;
use std::{fs, path::PathBuf};

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Document {
    pub path: PathBuf,
    pub description: String,
}

impl Default for Document {
    fn default() -> Self {
        Document {
            path: PathBuf::new(),
            description: String::new(),
        }
    }
}

impl Document {
    pub fn get_markup_language(&self) -> SupportedMarkup {
        match self.path.extension().unwrap().to_str().unwrap() {
            "md" | "markdown" => SupportedMarkup::Markdown,
            "txt" => SupportedMarkup::Text,
            _ => panic!("Unsupported markup format."),
        }
    }

    pub fn read(&self) -> String {
        fs::read_to_string(&self.path).expect("Error reading file {self.path}")
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub enum SupportedMarkup {
    //Asciidoc,
    Markdown,
    Text,
}
