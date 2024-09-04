use std::path::PathBuf;

use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Document {
    pub path: PathBuf
}

#[derive(Debug, Serialize, Deserialize)]
pub enum SupportedMarkup {
    //Asciidoc,
    Markdown,
    Text
}
