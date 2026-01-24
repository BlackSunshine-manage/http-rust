


#[test]
fn test_name_not_changed() {
    let vidio_with_typical_name = Video::new("TypicalName").name();
    assert_eq!(vidio_with_typical_name, "TypicalName");
}