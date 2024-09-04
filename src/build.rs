use core::fmt;

use clap::ValueEnum;

#[derive(Debug, ValueEnum, Clone, Copy, PartialEq, Eq)]
pub enum BuildTargets {
    Html,
    Word,
    Pdf,
}

impl fmt::Display for BuildTargets {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            BuildTargets::Html => write!(f, "html"),
            BuildTargets::Word => write!(f, "word"),
            BuildTargets::Pdf => write!(f, "pdf"),
        }
    }
}
