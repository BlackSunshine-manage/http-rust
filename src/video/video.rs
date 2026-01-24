use crate::HasName::HasName;

pub struct Video { 
    name: String
}

impl HasName for Video {
    fn new(name: String) -> Self {
        Video {name}
    }

    fn name(&self) -> &str {
        &self.name
    }
}