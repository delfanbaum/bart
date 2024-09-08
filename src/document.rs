use core::panic;
use std::{fs, path::PathBuf};

use crate::{build, project::SupportedMarkup};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Document {
    pub path: PathBuf,
    pub description: String,
    pub word_count: usize,
}

impl Default for Document {
    fn default() -> Self {
        Document {
            path: PathBuf::new(),
            description: String::new(),
            word_count: 0,
        }
    }
}

impl Document {
    pub fn get_markup_language(&self) -> SupportedMarkup {
        match self.path.extension().unwrap().to_str().unwrap() {
            "adoc" | "asciidoc" => SupportedMarkup::Asciidoc,
            "md" | "markdown" => SupportedMarkup::Markdown,
            "txt" => SupportedMarkup::Text,
            _ => panic!("Filetype not supported"),
        }
    }

    pub fn read(&self) -> String {
        fs::read_to_string(&self.path).expect("Error reading file {self.path}")
    }

    /// Counts the number of words (in the body <p> text), updates self, and returns for
    /// consumption elsewhere.
    /// Probably this needs to go on the project, since we don't necessarily need the document to
    /// be aware of its markup
    pub fn update_count(&mut self) {
        let html = build::to_html(&self.read(), &self.get_markup_language());
        self.word_count = build::count_words(&html);
    }
}
